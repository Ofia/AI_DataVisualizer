// Global state
let currentFile = null;
let currentFilepath = null;
let currentTemplate = 'professional';
let currentProvider = 'huggingface'; // Hard-coded to use free Hugging Face model
let currentAnalysis = null;

// DOM elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadStatus = document.getElementById('uploadStatus');
const statusText = document.getElementById('statusText');
const templateSection = document.getElementById('templateSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');

// Drag and drop functionality
dropZone.addEventListener('click', () => {
    fileInput.click();
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Handle file upload
async function handleFile(file) {
    currentFile = file;

    const formData = new FormData();
    formData.append('file', file);

    try {
        statusText.textContent = 'Uploading file...';
        uploadStatus.style.display = 'block';

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            statusText.textContent = `File uploaded: ${data.filename}`;
            currentFilepath = data.filepath;

            // Show template section
            templateSection.style.display = 'block';
            templateSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            statusText.textContent = `Error: ${data.error}`;
            uploadStatus.style.backgroundColor = '#F8D7DA';
        }
    } catch (error) {
        statusText.textContent = `Error: ${error.message}`;
        uploadStatus.style.backgroundColor = '#F8D7DA';
    }
}

// Select template
function selectTemplate(template) {
    currentTemplate = template;

    // Update UI
    document.querySelectorAll('.template-card').forEach(card => {
        card.classList.remove('active');
    });

    const selectedCard = document.querySelector(`[data-template="${template}"]`);
    if (selectedCard) {
        selectedCard.classList.add('active');
    }

    // If we already have analysis, regenerate with new template
    if (currentAnalysis) {
        regenerateVisualization();
    }
}

// Progress tracking
let progressInterval = null;
let holdMessageTimeout1 = null;
let holdMessageTimeout2 = null;
let holdMessageTimeout3 = null;
let progressStages = [
    { percent: 15, duration: 1000, text: "Processing your data...", stage: "Extracting and validating data structure", stageNum: 1 },
    { percent: 30, duration: 2000, text: "AI is analyzing patterns...", stage: "Claude is reading your data", stageNum: 2 },
    { percent: 50, duration: 3000, text: "AI is analyzing patterns...", stage: "Identifying insights and trends", stageNum: 2 },
    { percent: 70, duration: 3000, text: "AI is analyzing patterns...", stage: "Determining optimal visualizations", stageNum: 2 },
    { percent: 85, duration: 2000, text: "Generating visualizations...", stage: "Creating interactive charts", stageNum: 3 },
    { percent: 95, duration: 1000, text: "Finalizing...", stage: "Applying theme and polish", stageNum: 4 }
];

function updateProgress(percent, text, stage, stageNum) {
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');
    const progressText = document.getElementById('progressText');
    const progressStage = document.getElementById('progressStage');

    progressBar.style.width = percent + '%';
    progressPercent.textContent = percent + '%';
    progressText.textContent = text;
    progressStage.textContent = stage;

    // Update stage items
    for (let i = 1; i <= 4; i++) {
        const stageItem = document.getElementById('stage' + i);
        stageItem.classList.remove('active', 'completed');

        if (i < stageNum) {
            stageItem.classList.add('completed');
        } else if (i === stageNum) {
            stageItem.classList.add('active');
        }
    }
}

function updateProgressText(text, makeSmaller = false) {
    const progressText = document.getElementById('progressText');
    progressText.textContent = text;

    if (makeSmaller) {
        progressText.classList.add('smaller');
    } else {
        progressText.classList.remove('smaller');
    }
}

function startProgressSimulation() {
    // Reset progress
    updateProgress(0, "Initializing...", "Starting analysis", 1);

    let currentStage = 0;

    function advanceProgress() {
        if (currentStage < progressStages.length) {
            const stage = progressStages[currentStage];
            updateProgress(stage.percent, stage.text, stage.stage, stage.stageNum);

            // When we hit 95%, cycle through the hold messages in the progress text (above bar) (4 seconds each)
            if (stage.percent === 95) {
                holdMessageTimeout1 = setTimeout(() => {
                    updateProgressText("Hold on friend, I'm not stuck!", true);
                }, 1000);

                holdMessageTimeout2 = setTimeout(() => {
                    updateProgressText("We're baking the charts for you, just a few more seconds...", true);
                }, 5000); // 1 + 4 seconds

                holdMessageTimeout3 = setTimeout(() => {
                    updateProgressText("Your data is flowing through fiber-optic cables around the entire world — it's almost there!", true);
                }, 9000); // 5 + 4 seconds

                // After all messages, go back to "Finalizing..." with normal size
                setTimeout(() => {
                    updateProgressText("Finalizing...", false);
                }, 13000); // 9 + 4 seconds
            }

            currentStage++;
            progressInterval = setTimeout(advanceProgress, stage.duration);
        }
    }

    advanceProgress();
}

function stopProgressSimulation() {
    if (progressInterval) {
        clearTimeout(progressInterval);
        progressInterval = null;
    }
    if (holdMessageTimeout1) {
        clearTimeout(holdMessageTimeout1);
        holdMessageTimeout1 = null;
    }
    if (holdMessageTimeout2) {
        clearTimeout(holdMessageTimeout2);
        holdMessageTimeout2 = null;
    }
    if (holdMessageTimeout3) {
        clearTimeout(holdMessageTimeout3);
        holdMessageTimeout3 = null;
    }
    // Set to 100% when done
    updateProgress(100, "Complete!", "Analysis finished", 4);
}

// Analyze data
async function analyzeData() {
    if (!currentFilepath) {
        alert('Please upload a file first');
        return;
    }

    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');

    try {
        // Show loading
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
        analyzeBtn.disabled = true;

        loadingSection.style.display = 'block';
        loadingSection.scrollIntoView({ behavior: 'smooth' });

        // Start progress simulation
        startProgressSimulation();

        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: currentFilepath,
                provider: currentProvider,
                template: currentTemplate
            })
        });

        const data = await response.json();

        // Stop progress simulation
        stopProgressSimulation();

        if (data.success) {
            currentAnalysis = data.analysis;

            // Small delay to show 100%
            setTimeout(() => {
                displayResults(data);
            }, 500);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        stopProgressSimulation();
        alert(`Error: ${error.message}`);
    } finally {
        // Hide loading after a short delay
        setTimeout(() => {
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            analyzeBtn.disabled = false;
            loadingSection.style.display = 'none';
        }, 600);
    }
}

// Regenerate visualization with new template
async function regenerateVisualization() {
    if (!currentFilepath || !currentAnalysis) {
        return;
    }

    try {
        loadingSection.style.display = 'block';

        const response = await fetch('/regenerate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: currentFilepath,
                template: currentTemplate,
                analysis: currentAnalysis
            })
        });

        const data = await response.json();

        if (data.success) {
            displayResults({
                analysis: currentAnalysis,
                visualizations: data.visualizations
            });
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        loadingSection.style.display = 'none';
    }
}

// Display results
function displayResults(data) {
    const { analysis, visualizations } = data;

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    // Display summary
    document.getElementById('summaryText').textContent = visualizations.summary || analysis.summary || 'No summary available';

    // Display insights
    const insightsList = document.getElementById('insightsList');
    insightsList.innerHTML = '';
    const insights = visualizations.insights || analysis.insights || [];
    insights.forEach(insight => {
        const li = document.createElement('li');
        li.textContent = insight;
        insightsList.appendChild(li);
    });

    // Display charts
    const chartsContainer = document.getElementById('chartsContainer');
    chartsContainer.innerHTML = '';

    visualizations.charts.forEach((chart, index) => {
        const chartItem = document.createElement('div');
        chartItem.className = 'chart-item';

        // Create a temporary div to parse the HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = chart.html;

        // Extract the chart div and script
        const chartDiv = tempDiv.querySelector('div');
        const scriptTag = tempDiv.querySelector('script');

        // Add the chart div
        if (chartDiv) {
            chartItem.appendChild(chartDiv.cloneNode(true));
        }

        // Add description
        const descDiv = document.createElement('div');
        descDiv.className = 'chart-description';
        descDiv.textContent = chart.description;
        chartItem.appendChild(descDiv);

        chartsContainer.appendChild(chartItem);

        // Execute the script manually
        if (scriptTag) {
            const newScript = document.createElement('script');
            newScript.text = scriptTag.textContent;
            document.body.appendChild(newScript);
        }
    });
}

// Export to PDF (Data-Driven)
async function exportPDF() {
    const exportBtn = document.querySelector('.export-btn');
    const originalText = exportBtn.textContent;

    try {
        exportBtn.textContent = 'Generating PDF...';
        exportBtn.disabled = true;

        // Initialize jsPDF
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // PDF Settings
        const margin = 15;
        const pageWidth = doc.internal.pageSize.getWidth(); // 210mm
        const pageHeight = doc.internal.pageSize.getHeight(); // 297mm
        const contentWidth = pageWidth - (margin * 2);
        let yPos = margin;

        // Helper to add new page if needed
        function checkPageBreak(heightNeeded) {
            if (yPos + heightNeeded > pageHeight - margin) {
                doc.addPage();
                yPos = margin;
                return true;
            }
            return false;
        }

        // --- 1. Header ---
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(22);
        doc.setTextColor(44, 62, 80); // #2C3E50
        doc.text("AI Data Analysis Report", margin, yPos + 8);
        yPos += 15;

        doc.setFont('helvetica', 'normal');
        doc.setFontSize(10);
        doc.setTextColor(100, 100, 100);
        doc.text(`Generated on ${new Date().toLocaleString()}`, margin, yPos);
        yPos += 10;

        doc.setDrawColor(200, 200, 200);
        doc.line(margin, yPos, pageWidth - margin, yPos);
        yPos += 10;

        // --- 2. Summary ---
        const summaryText = document.getElementById('summaryText').textContent;
        if (summaryText) {
            doc.setFont('helvetica', 'bold');
            doc.setFontSize(14);
            doc.setTextColor(44, 62, 80);
            doc.text("Executive Summary", margin, yPos);
            yPos += 8;

            doc.setFont('helvetica', 'normal');
            doc.setFontSize(11);
            doc.setTextColor(60, 60, 60);

            const splitSummary = doc.splitTextToSize(summaryText, contentWidth);
            doc.text(splitSummary, margin, yPos);
            yPos += (splitSummary.length * 6) + 10;
        }

        // --- 3. Insights ---
        const insightsList = document.querySelectorAll('#insightsList li');
        if (insightsList.length > 0) {
            checkPageBreak(30); // Ensure header fits

            doc.setFont('helvetica', 'bold');
            doc.setFontSize(14);
            doc.setTextColor(44, 62, 80);
            doc.text("Key Insights", margin, yPos);
            yPos += 8;

            doc.setFont('helvetica', 'normal');
            doc.setFontSize(11);
            doc.setTextColor(60, 60, 60);

            insightsList.forEach(li => {
                const text = "• " + li.textContent;
                const splitText = doc.splitTextToSize(text, contentWidth);

                checkPageBreak(splitText.length * 6);
                doc.text(splitText, margin, yPos);
                yPos += (splitText.length * 6) + 2;
            });
            yPos += 10;
        }

        // --- 4. Charts ---
        const chartItems = document.querySelectorAll('.chart-item');

        for (let i = 0; i < chartItems.length; i++) {
            const item = chartItems[i];
            const chartDiv = item.querySelector('.plotly-graph-div'); // Plotly creates this class
            const descDiv = item.querySelector('.chart-description');

            if (chartDiv) {
                // Get chart image using Plotly's native export
                // This is much better than html2canvas as it handles SVG correctly
                const imgData = await Plotly.toImage(chartDiv, {
                    format: 'png',
                    width: 1000, // High res
                    height: 600
                });

                // Calculate dimensions to fit PDF width
                const imgHeight = (600 / 1000) * contentWidth;

                // Check space for chart + description
                // If not enough space, start new page
                checkPageBreak(imgHeight + 40);

                // Add Chart
                doc.addImage(imgData, 'PNG', margin, yPos, contentWidth, imgHeight);
                yPos += imgHeight + 5;

                // Add Description
                if (descDiv) {
                    doc.setFont('helvetica', 'italic');
                    doc.setFontSize(10);
                    doc.setTextColor(80, 80, 80);

                    const splitDesc = doc.splitTextToSize(descDiv.textContent, contentWidth);
                    checkPageBreak(splitDesc.length * 5);

                    doc.text(splitDesc, margin, yPos);
                    yPos += (splitDesc.length * 5) + 15;
                } else {
                    yPos += 15;
                }
            }
        }

        // Save
        doc.save('AI_Data_Analysis_Report.pdf');

    } catch (error) {
        console.error("PDF Export Error:", error);
        alert("Error generating PDF: " + error.message);
    } finally {
        exportBtn.textContent = originalText;
        exportBtn.disabled = false;
    }
}

// Initialize theme
document.addEventListener('DOMContentLoaded', () => {

    // Theme Toggle Logic
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    // Check for saved theme or default to 00s (checked)
    const savedTheme = localStorage.getItem('theme') || 'theme-00s';

    if (savedTheme === 'theme-00s') {
        body.classList.add('theme-00s');
        body.classList.remove('theme-90s');
        themeToggle.checked = true;
    } else {
        body.classList.add('theme-90s');
        body.classList.remove('theme-00s');
        themeToggle.checked = false;
    }

    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            // 00s Mode
            body.classList.add('theme-00s');
            body.classList.remove('theme-90s');
            localStorage.setItem('theme', 'theme-00s');
        } else {
            // 90s Mode
            body.classList.add('theme-90s');
            body.classList.remove('theme-00s');
            localStorage.setItem('theme', 'theme-90s');
        }
    });
});
