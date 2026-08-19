const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const previewContainer = document.querySelector(".preview-container");

const predictButton = document.getElementById("predictButton");

const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");

const resultCard = document.getElementById("result");

const diseaseElement = document.getElementById("disease");
const confidenceElement = document.getElementById("confidence");

const explanationElement = document.getElementById("explanation");
const symptomsElement = document.getElementById("symptoms");
const managementElement = document.getElementById("management");


const API_URL = "/predict";


imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    preview.src = URL.createObjectURL(file);

    previewContainer.classList.add("show");

    predictButton.disabled = false;

    resultCard.classList.remove("show");

    errorBox.textContent = "";
});


predictButton.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        errorBox.textContent = "Please select an image first.";
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    predictButton.disabled = true;

    loading.classList.add("show");

    errorBox.textContent = "";

    resultCard.classList.remove("show");


    try {

        const response = await fetch(
            API_URL,
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {
            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data = await response.json();


        diseaseElement.textContent =
            data.disease.replaceAll("_", " ");


        confidenceElement.textContent =
            `${Number(data.confidence_percentage).toFixed(2)}%`;


        explanationElement.textContent =
            data.explanation;


        symptomsElement.textContent =
            data.symptoms;


        managementElement.textContent =
            data.management;


        resultCard.classList.add("show");


    } catch (error) {

        console.error(error);

        errorBox.textContent =
            "Unable to connect to AgriVision AI. Make sure the API server is running.";

    } finally {

        loading.classList.remove("show");

        predictButton.disabled = false;

    }

});