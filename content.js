async function summarizeTOS() {
    const text = document.body.innerText;
    if (text.length < 1000 || !text.toLowerCase().includes("terms")) return;

    // Create a loading message
    const loadingOverlay = document.createElement("div");
    loadingOverlay.style = `
        position: fixed;
        top: 10px;
        right: 10px;
        width: 400px;
        height: 200px;
        background: white;
        border: 3px solid #ff5733;
        padding: 15px;
        z-index: 99999;
        font-family: Arial, sans-serif;
        font-size: 16px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        overflow-y: auto;
        text-align: center;
    `;
    loadingOverlay.innerHTML = `
        <h3>🤖 AI TOS Analyzer</h3>
        <p>Before you click <strong>Accept</strong>, let's analyze those Terms of Service using the power of AI! 🚀</p>
        <p>Hang tight... we're diving into the legal mumbo jumbo. 📜🔍</p>
    `;
    document.body.appendChild(loadingOverlay);

    // Send text to the AI
    try {
        const response = await fetch("http://127.0.0.1:5000/summarize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        
        // Replace loading message with actual summary
        loadingOverlay.innerHTML = `
            <h3>🧠 AI TOS Summary</h3>
            <p><strong>Key Points:</strong></p>
            ${formatAsList(data.summary)}
            <br>
            <p style="color: red;"><strong>Red Flags:</strong></p>
            ${formatAsList(data.redFlags)}
        `;
        loadingOverlay.style.height = "500px"; // Expand for more readable content
        loadingOverlay.style.overflowY = "scroll"; // Enable scrolling

    } catch (error) {
        loadingOverlay.innerHTML = `<h3>⚠️ Error</h3><p>Failed to analyze TOS. Please try again.</p>`;
        console.error("AI Analysis Error:", error);
    }
}

// Helper function to format text into an ordered list
function formatAsList(text) {
    const items = text.split(/\d+\.\s/).filter(Boolean); // Split on numbers but keep content
    return "<ol style='text-align:left; font-size:14px; line-height:1.5;'><li>" + 
           items.join("</li><li>") + "</li></ol>"; // Convert to list
}

summarizeTOS();
