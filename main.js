// document.getElementById('uploadForm').addEventListener('submit', async function (event) {
//     event.preventDefault();  // Prevent default form submission

//     let formData = new FormData();
//     let imageFile = document.getElementById('imageUpload').files[0];

//     if (!imageFile) {
//         alert("Please select an image before submitting!");
//         return;
//     }

//     formData.append("file", imageFile);

//     try {
//         let response = await fetch('/predict', {
//             method: 'POST',
//             body: formData
//         });

//         if (!response.ok) {
//             throw new Error(`Server error: ${response.status}`);
//         }

//         let result = await response.json();

//         // Ensure the response contains correct values
//         if (!result.prediction || typeof result.confidence === 'undefined') {
//             throw new Error("Invalid response format from server.");
//         }

//         document.getElementById('predictionResult').innerHTML = `
//             <h3>✅ Prediction: ${result.prediction}</h3>
//             <p>Confidence Score: ${result.confidence.toFixed(2)}%</p>
//         `;
//     } catch (error) {
//         console.error("Error:", error);
//         document.getElementById('predictionResult').innerHTML = "<p style='color:red;'>❌ Error processing the image. Please try again.</p>";
//     }
// });
