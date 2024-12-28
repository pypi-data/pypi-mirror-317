document.addEventListener("DOMContentLoaded", function() {
    // =========================
    // HTML Toggle Functionality
    // =========================
    (function() {
        const editor = document.getElementById('editor_content_new');
        const editHTMLButton = document.querySelector('[data-command="editHTML"]'); // Button for HTML editing
        let isHTMLView = false; // Track if the editor is in HTML view mode

        // Function to format HTML
        function format(html) {
            var tab = '\t';
            var result = '';
            var indent = '';

            html.split(/>\s*</).forEach(function(element) {
                if (element.match(/^\/\w/)) {
                    indent = indent.substring(tab.length);
                }

                result += indent + '<' + element + '>\r\n';

                if (element.match(/^<?\w[^>]*[^\/]$/) && !element.startsWith("input")) {
                    indent += tab;
                }
            });

            return result.substring(1, result.length - 3);
        }

        // Toggle HTML/Visual mode
        editHTMLButton.addEventListener('click', function() {
            if (isHTMLView) {
                // Switch from HTML view to visual view
                editor.innerHTML = editor.textContent; // Replace text with HTML content
                editor.contentEditable = "true"; // Make editor contenteditable again
                isHTMLView = false;
            } else {
                // Switch from visual view to HTML view
                const rawHTML = editor.innerHTML; // Get the current HTML content
                const formattedHTML = format(rawHTML); // Format the HTML using the format function
                editor.textContent = formattedHTML; // Replace HTML content with formatted text
                editor.contentEditable = "true"; // Make editor contenteditable again
                isHTMLView = true;
            }
        });
})();

// =========================
// Table Insertion Functionality
// =========================
(function() {
        const editor = document.getElementById('editor_content_new');
        const insertTableButton = document.getElementById('insertTableButton');
        const tableGridContainer = document.getElementById('tableGridContainer');
        let savedRange = null; // Store the selection range here

        // Create the grid for table selection
        function createTableGrid() {
            tableGridContainer.innerHTML = ''; // Clear any previous grid content

            // Create a 10x10 grid
            for (let i = 1; i <= 10; i++) {
                const rowDiv = document.createElement('div');
                rowDiv.style.display = 'flex';

                for (let j = 1; j <= 10; j++) {
                    const cellDiv = document.createElement('div');
                    cellDiv.style.width = '20px';
                    cellDiv.style.height = '20px';
                    cellDiv.style.border = '1px solid #ccc';
                    cellDiv.style.cursor = 'pointer';

                    // Hover and selection logic
                    cellDiv.addEventListener('mouseover', () => {
                        highlightGrid(i, j);
                    });

                    cellDiv.addEventListener('click', () => {
                        restoreSelection(); // Restore the cursor position before inserting the table
                        insertTable(i, j);
                        tableGridContainer.style.display = 'none'; // Hide grid after selection
                    });

                    rowDiv.appendChild(cellDiv);
                }
                tableGridContainer.appendChild(rowDiv);
            }
        }

        // Highlight the grid cells based on user hover
        function highlightGrid(rows, cols) {
            const rowDivs = tableGridContainer.children; // Select all row divs

            // Iterate over each row
            for (let r = 0; r < rowDivs.length; r++) {
                const rowDiv = rowDivs[r];
                const cells = rowDiv.children;

                // Iterate over each cell in the row
                for (let c = 0; c < cells.length; c++) {
                    const cell = cells[c];
                    
                    // Highlight cell if it's within the selected rows and columns
                    if (r < rows && c < cols) {
                        cell.style.backgroundColor = '#007BFF';
                    } else {
                        cell.style.backgroundColor = '#fff';
                    }
                }
            }
        }

        // Insert table into the contenteditable div based on the selected rows and columns
        function insertTable(rows, cols) {
            // Create the table container
            const tableContainer = document.createElement('div');
            tableContainer.style.display = 'table';
            tableContainer.style.width = '100%';
            tableContainer.style.borderCollapse = 'collapse';
            tableContainer.style.margin = '10px 0';

            // Add rows and columns to the table container
            for (let r = 0; r < rows; r++) {
                // Create a div for each row
                const rowDiv = document.createElement('div');
                rowDiv.style.display = 'table-row';

                for (let c = 0; c < cols; c++) {
                    // Create a div for each cell
                    const cellDiv = document.createElement('div');
                    cellDiv.style.display = 'table-cell';
                    cellDiv.style.border = '1px solid #ccc';
                    cellDiv.style.padding = '8px';
                    cellDiv.style.textAlign = 'left';
                    cellDiv.textContent = ' '; // Placeholder content for each cell
					cellDiv.style.maxWidth = '50px'; // Set a minimum width for the cell


                    rowDiv.appendChild(cellDiv); // Add the cell to the row
                }

                tableContainer.appendChild(rowDiv); // Add the row to the table
            }

            // Insert the table container at the cursor position
            insertAtCursor(editor, tableContainer);

            // Update the corresponding textarea if necessary
            const textarea = document.querySelector(`textarea[name="insertTable"]`);
            if (textarea) {
                textarea.value = editor.innerHTML;
            }
        }

        // Function to insert content at the current cursor position
        function insertAtCursor(editor, element) {
            let sel, range;

            if (window.getSelection) {
                sel = window.getSelection();
                // Use saved range if available
                range = savedRange || sel.getRangeAt(0);

                range.deleteContents();

                // Create a DocumentFragment to insert the table safely
                const frag = document.createDocumentFragment();
                frag.appendChild(element);

                // Insert the fragment containing the table
                range.insertNode(frag);

                // Move the cursor after the inserted element
                range = range.cloneRange();
                range.setStartAfter(element);
                range.collapse(true);

                // Clear current selection and add the new range
                sel.removeAllRanges();
                sel.addRange(range);
            } else if (document.selection && document.selection.createRange) {
                // For older versions of IE
                range = document.selection.createRange();
                range.pasteHTML(element.outerHTML);
            }

            savedRange = null; // Clear the saved range after use
        }

        // Save the selection before showing the grid
        function saveSelection() {
            const sel = window.getSelection();
            if (sel.rangeCount > 0) {
                savedRange = sel.getRangeAt(0);
            }
        }

        // Restore the saved selection
        function restoreSelection() {
            if (savedRange) {
                const sel = window.getSelection();
                sel.removeAllRanges();
                sel.addRange(savedRange);
            }
        }

        // Initialize the grid only once
        createTableGrid();

        // Save selection when the button is clicked and show the grid
        insertTableButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent the event from propagating and immediately hiding the grid
            saveSelection(); // Save the cursor position

            if (tableGridContainer.style.display === 'none' || !tableGridContainer.style.display) {
                tableGridContainer.style.display = 'block';
            } else {
                tableGridContainer.style.display = 'none';
            }

            // Position the grid container near the button
            const rect = insertTableButton.getBoundingClientRect();
            tableGridContainer.style.top = `${rect.bottom + window.scrollY + 10}px`;
            tableGridContainer.style.left = `${rect.left + window.scrollX}px`;
        });

        // Hide the grid if clicking outside
        document.addEventListener('click', (e) => {
            if (!tableGridContainer.contains(e.target) && e.target !== insertTableButton) {
                tableGridContainer.style.display = 'none';
            }
        });

        // Prevent the click event from hiding the grid when clicking inside it
        tableGridContainer.addEventListener('click', (e) => {
            e.stopPropagation();
        });
})();

// =========================
// Custom WYSIWYG Editor Initialization
// =========================
(function() {
        /**
         * Retrieves the value of a specified cookie.
         * @param {string} name - The name of the cookie.
         * @returns {string|null} The cookie value or null if not found.
         */
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    cookie = cookie.trim();
                    if (cookie.startsWith(name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        /**
         * Validates whether a given string is a well-formed URL.
         * @param {string} string - The URL string to validate.
         * @returns {boolean} True if valid, else false.
         */
        function isValidURL(string) {
            try {
                new URL(string);
                return true;
            } catch (_) {
                return false;  
            }
        }

        /**
         * Inserts an element (e.g., image, iframe, link) at the current cursor position within the editor.
         * @param {HTMLElement} editor - The editable div.
         * @param {HTMLElement} element - The element to insert.
         */
        function insertAtCursor(editor, element) {
            let sel, range;
            if (window.getSelection) {
                sel = window.getSelection();
                if (sel.getRangeAt && sel.rangeCount) {
                    range = sel.getRangeAt(0);
                    range.deleteContents();
                    range.insertNode(element);

                    // Move the cursor after the inserted element
                    range.setStartAfter(element);
                    range.collapse(true);
                    sel.removeAllRanges();
                    sel.addRange(range);
                }
            } else if (document.selection && document.selection.createRange) {
                range = document.selection.createRange();
                range.pasteHTML(element.outerHTML);
            }
        }

        /**
         * Handles the image upload process by sending the file to the server and inserting the returned image URL.
         * @param {File} file - The image file to upload.
         * @param {string} fieldName - The unique identifier for the editor.
         * @param {HTMLElement} editor - The editable div.
         */
        function uploadImage(file, fieldName, editor) {
            const formData = new FormData();
            formData.append('image', file);

            const csrftoken = getCookie('csrftoken');

            fetch("/unchained_editor/upload_image/", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.url) {
                    insertImage(data.url, fieldName, editor);
                } else if (data.error) {
                    alert(data.error);
                } else {
                    alert("Image upload failed.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while uploading the image.");
            });
        }

        /**
         * Inserts an uploaded image into the editor at the cursor position.
         * @param {string} url - The URL of the uploaded image.
         * @param {string} fieldName - The unique identifier for the editor.
         * @param {HTMLElement} editor - The editable div.
         */
        function insertImage(url, fieldName, editor) {
            const img = document.createElement('img');
            img.src = url;
            img.alt = 'Uploaded Image';
            img.style.maxWidth = '100%'; // Ensures image fits within editor

            // Insert image at the cursor position
            insertAtCursor(editor, img);

            // Update the corresponding textarea
            const textarea = document.querySelector(`textarea[name="${fieldName}"]`);
            if (textarea) {
                textarea.value = editor.innerHTML;
            }
        }

        /**
         * Inserts a globe icon representing an image URL into the editor.
         * @param {string} url - The URL of the image.
         * @param {string} fieldName - The unique identifier for the editor.
         * @param {HTMLElement} editor - The editable div.
         */
		 function insertImageURL(url, fieldName, editor) {
			// Create the image element
			const img = document.createElement('img');
			img.src = url;
			img.alt = 'Inserted Image';
			img.style.maxWidth = '100%'; // Ensure the image doesn't overflow the editor's width
			img.style.height = 'auto';
			
			// Insert image at the cursor position
			insertAtCursor(editor, img);

			// Update the corresponding textarea
			const textarea = document.querySelector(`textarea[name="${fieldName}"]`);
			if (textarea) {
				textarea.value = editor.innerHTML;
			}
		}

        /**
         * Inserts a video iframe into the editor at the cursor position.
         * @param {string} url - The URL of the video.
         * @param {string} fieldName - The unique identifier for the editor.
         * @param {HTMLElement} editor - The editable div.
         */
        function insertVideo(url, fieldName, editor) {
            // Convert standard video URLs to embeddable iframe URLs
            const embedURL = convertToEmbedURL(url);
            if (!embedURL) {
                alert("Unsupported video URL format.");
                return;
            }

            const iframe = document.createElement('iframe');
            iframe.src = embedURL;
            iframe.width = "560";
            iframe.height = "315";
            iframe.frameBorder = "0";
            iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
            iframe.allowFullscreen = true;
            iframe.style.maxWidth = '100%'; // Ensures iframe fits within editor

            // Insert iframe at the cursor position
            insertAtCursor(editor, iframe);

            // Update the corresponding textarea
            const textarea = document.querySelector(`textarea[name="${fieldName}"]`);
            if (textarea) {
                textarea.value = editor.innerHTML;
            }
        }

        /**
         * Converts a standard video URL to an embeddable iframe URL.
         * Supports YouTube and Vimeo for this example.
         * @param {string} url - The standard video URL.
         * @returns {string|null} The embeddable iframe URL or null if unsupported.
         */
        function convertToEmbedURL(url) {
            let embedURL = null;
            const youtubeMatch = url.match(/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})/);
            const vimeoMatch = url.match(/(?:https?:\/\/)?(?:www\.)?vimeo\.com\/(\d+)/);

            if (youtubeMatch && youtubeMatch[1]) {
                embedURL = `https://www.youtube.com/embed/${youtubeMatch[1]}`;
            } else if (vimeoMatch && vimeoMatch[1]) {
                embedURL = `https://player.vimeo.com/video/${vimeoMatch[1]}`;
            }

            return embedURL;
        }

        /**
         * Inserts a table into the editor at the cursor position.
         * @param {number} rows - The number of rows for the table.
         * @param {number} cols - The number of columns for the table.
         * @param {string} fieldName - The unique identifier for the editor.
         * @param {HTMLElement} editor - The editable div.
         */
        function insertTable(rows, cols, fieldName, editor) {
			// Create the table element
			const table = document.createElement('table');
			table.style.width = '100%';
			table.style.borderCollapse = 'collapse';
			table.style.margin = '10px 0';

			// Create the table body
			const tbody = document.createElement('tbody');

			// Add rows and columns to the table
			for (let r = 0; r < rows; r++) {
				const tr = document.createElement('tr'); // Create a row
				for (let c = 0; c < cols; c++) {
					const td = document.createElement('td'); // Create a cell
					td.textContent = ' '; // Placeholder content for each cell
					td.style.border = '1px solid #ccc';
					td.style.padding = '8px';
					td.style.textAlign = 'left';
					tr.appendChild(td);
				}
				tbody.appendChild(tr);
			}

			table.appendChild(tbody);

			// Insert table at the cursor position
			insertAtCursor(editor, table);

			// Update the corresponding textarea
			const textarea = document.querySelector(`textarea[name="${fieldName}"]`);
			if (textarea) {
				textarea.value = editor.innerHTML;
			}
		}


        /**
         * Prompts the user to choose between uploading an image or inserting an image URL.
         * @param {string} fieldName - The unique identifier for the editor.
         */
        function openImageInsertionOptions(fieldName) {
            const option = prompt("Choose Image Insertion Method:\n1. Upload from Computer\n2. Insert Image URL\nEnter 1 or 2:");

            if (option === "1") {
                insertImageFromUpload(fieldName);
            } else if (option === "2") {
                insertImageFromURLPrompt(fieldName);
            } else {
                alert("Invalid option. Please enter 1 or 2.");
            }
        }



        /**
         * Prompts the user to enter an image URL and inserts it as a globe icon link.
         * @param {string} fieldName - The unique identifier for the editor.
         */
        function insertImageFromURLPrompt(fieldName) {
            const url = prompt("Enter the image URL:", "https://");
            if (url) {
                if (isValidURL(url)) {
                    const editor = document.querySelector(`#editor_${fieldName}`);
                    if (editor) {
                        insertImageURL(url, fieldName, editor);
                    }
                } else {
                    alert("Please enter a valid URL.");
                }
            }
        }

        /**
         * Triggers the hidden file input to allow the user to upload an image from their computer.
         * @param {string} fieldName - The unique identifier for the editor.
         */
        function insertImageFromUpload(fieldName) {
            const imageUploadInput = document.querySelector(`#imageUpload_${fieldName}`);
            if (imageUploadInput) {
                imageUploadInput.click();
            }
        }

        /**
         * Handles toolbar button commands such as bold, italic, underline, link, image insertion, and video insertion.
         * @param {string} command - The command to execute.
         * @param {string} fieldName - The unique identifier for the editor.
         * @param {HTMLElement} editor - The editable div.
         */
        function handleToolbarCommand(command, fieldName, editor) {
            const textarea = document.querySelector(`textarea[name="${fieldName}"]`);
            if (!textarea) return;

            if (command === 'createLink') {
                const url = prompt("Enter the link URL:", "https://");
                if (url) {
                    if (isValidURL(url)) {
                        document.execCommand(command, false, url);
                    } else {
                        alert("Please enter a valid URL.");
                    }
                }
            } else if (command === 'insertImage') {
                openImageInsertionOptions(fieldName);
            } else if (command === 'insertVideo') {
                insertVideoPrompt(fieldName);
            } else {
                document.execCommand(command, false, null);
            }

            // Update the corresponding textarea after executing the command
            textarea.value = editor.innerHTML;
        }

        /**
         * Prompts the user to enter a video URL and inserts it as an iframe.
         * @param {string} fieldName - The unique identifier for the editor.
         */
        function insertVideoPrompt(fieldName) {
            const url = prompt("Enter the video URL (YouTube or Vimeo):", "https://");
            if (url) {
                if (isValidURL(url)) {
                    const editor = document.querySelector(`#editor_${fieldName}`);
                    if (editor) {
                        insertVideo(url, fieldName, editor);
                    }
                } else {
                    alert("Please enter a valid URL.");
                }
            }
        }

		/**
		 * Checks if a value is a positive integer.
		 * @param {string} value - The value to check.
		 * @returns {boolean} - True if the value is a positive integer, false otherwise.
		 */
		function isPositiveInteger(value) {
			const number = Number(value);
			return Number.isInteger(number) && number > 0;
		}


        /**
         * Initializes the Custom WYSIWYG Editor for a given field.
         * @param {string} fieldName - The unique identifier for the editor.
         */
        function initializeCustomWYSIWYG(fieldName) {
            const editor = document.querySelector(`#editor_${fieldName}`);
            const textarea = document.querySelector(`textarea[name="${fieldName}"]`);
            const imageUploadInput = document.querySelector(`#imageUpload_${fieldName}`);
            const uploadImageButton = document.querySelector(`#uploadImageButton_${fieldName}`);
            const insertImageURLButton = document.querySelector(`#insertImageURLButton_${fieldName}`);
            const insertVideoButton = document.querySelector(`#insertVideoButton_${fieldName}`); // If you have a separate video button
			const insertTableButton = document.querySelector(`#insertTableButton_${fieldName}`); // If you have a separate table button

            if (!editor || !textarea) return;

            // Synchronize editor content with textarea
            editor.addEventListener('input', () => {
                textarea.value = editor.innerHTML;
            });

            // Initialize editor with existing content
            editor.innerHTML = textarea.value;

            // Handle toolbar button clicks specific to this editor
            const toolbarButtons = editor.parentElement.querySelectorAll('.toolbar button[data-command]');
            toolbarButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const command = button.getAttribute('data-command');
                    handleToolbarCommand(command, fieldName, editor);
                });
            });

            // Handle image upload button click
            if (uploadImageButton && imageUploadInput) {
                uploadImageButton.addEventListener('click', () => {
                    imageUploadInput.click();
                });

                imageUploadInput.addEventListener('change', function() {
                    const file = this.files[0];
                    if (file) {
                        if (file.type.startsWith('image/')) {
                            uploadImage(file, fieldName, editor);
                        } else {
                            alert("Please select a valid image file.");
                        }
                    }

                    // Reset the input value to allow re-uploading the same file if needed
                    this.value = "";
                });
            }

            // Handle Insert Image URL button click
            if (insertImageURLButton) {
                insertImageURLButton.addEventListener('click', () => {
                    const url = prompt("Enter the image URL:", "https://");
                    if (url) {
                        if (isValidURL(url)) {
                            insertImageURL(url, fieldName, editor);
                        } else {
                            alert("Please enter a valid URL.");
                        }
                    }
                });
            }

            // Handle Insert Video button click
            if (insertVideoButton) {
                insertVideoButton.addEventListener('click', () => {
                    const url = prompt("Enter the video URL (YouTube or Vimeo):", "https://");
                    if (url) {
                        if (isValidURL(url)) {
                            insertVideo(url, fieldName, editor);
                        } else {
                            alert("Please enter a valid URL.");
                        }
                    }
                });
            }

			// Handle Insert Table button click
			if (insertTableButton) {
				insertTableButton.addEventListener('click', () => {
					const rows = prompt("Enter the number of rows:", "2");
					const cols = prompt("Enter the number of columns:", "2");

					// Validate input
					if (rows && cols && isPositiveInteger(rows) && isPositiveInteger(cols)) {
						insertTable(parseInt(rows, 10), parseInt(cols, 10), fieldName, editor);
					} else {
						alert("Please enter valid positive integers for rows and columns.");
					}
				});
			}

        }

        /**
         * Initializes all Custom WYSIWYG Editors present on the page.
         */
        function initializeCustomWYSIWYGEditors() {
            // Select all editor containers on the page
            const editorContainers = document.querySelectorAll('.editor-container');

            editorContainers.forEach(container => {
                const fieldName = container.getAttribute('data-field-name');
                if (fieldName) {
                    initializeCustomWYSIWYG(fieldName);
                }
            });
        }

        // Initialize all editors once the DOM is fully loaded
        initializeCustomWYSIWYGEditors();
    })();
});