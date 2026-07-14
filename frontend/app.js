const API_URL = "http://127.0.0.1:8000";

let editingId = null;

const form = document.getElementById("noteForm");
const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");
const submitButton = form.querySelector("button");
const notesDiv = document.getElementById("notes");

loadNotes();

async function loadNotes() {

    try {

        const response = await fetch(`${API_URL}/notes`);

        if (!response.ok) {
            throw new Error("Failed to fetch notes.");
        }

        const notes = await response.json();

        notesDiv.innerHTML = "";

        notes.forEach(note => {

            const card = document.createElement("div");
            card.className = "note";

            const title = document.createElement("h3");
            title.textContent = note.title;

            const content = document.createElement("p");
            content.textContent = note.content;

            const editButton = document.createElement("button");
            editButton.textContent = "Edit";

            editButton.addEventListener("click", () => {

                editingId = note.id;

                titleInput.value = note.title;
                contentInput.value = note.content;

                submitButton.textContent = "Update Note";

            });

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";

            deleteButton.addEventListener("click", async () => {

                const confirmDelete = confirm("Delete this note?");

                if (!confirmDelete) return;

                try {

                    const response = await fetch(`${API_URL}/notes/${note.id}`, {
                        method: "DELETE"
                    });

                    if (!response.ok) {
                        throw new Error("Failed to delete note.");
                    }

                    loadNotes();

                } catch (error) {

                    console.error(error);
                    alert("Failed to delete note.");

                }

            });

            card.appendChild(title);
            card.appendChild(content);
            card.appendChild(editButton);
            card.appendChild(deleteButton);

            notesDiv.appendChild(card);

        });

    } catch (error) {

        console.error(error);
        notesDiv.innerHTML = "<p>Unable to load notes. Please check if the backend is running.</p>";

    }

}

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const note = {

        title: titleInput.value,
        content: contentInput.value

    };

    try {

        let response;

        if (editingId === null) {

            response = await fetch(`${API_URL}/notes`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(note)

            });

        }
        else {

            response = await fetch(`${API_URL}/notes/${editingId}`, {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(note)

            });

        }

        if (!response.ok) {
            throw new Error("Operation failed.");
        }

        if (editingId !== null) {
            editingId = null;
            submitButton.textContent = "Add Note";
        }

        form.reset();

        loadNotes();

    } catch (error) {

        console.error(error);
        alert("Operation failed.");

    }

});