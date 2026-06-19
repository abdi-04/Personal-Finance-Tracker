// NAVIGATION & SECTION LOADER
// Handles menu highlighting and loading page sections
// dynamically from the server without a full page reload.


// DOM ELEMENT REFERENCES
// Grab the container where section content will be injected
const sectionContainer = document.getElementById("section-container");


// MENU FUNCTIONS 

// Highlights the menu item that matches the current section,
// and removes the highlight from all others
function setActiveMenu(section) {
  document.querySelectorAll(".menu-item").forEach(item => {
    // Toggle the "active" class — true if this item matches the section
    item.classList.toggle("active", item.dataset.section === section);
  });
}


// SECTION LOADER

// Fetches a section's HTML from the server and injects it into the page.
// Uses async/await so the code reads top-to-bottom like normal code,
// instead of chaining .then() calls.
async function loadSection(section) {
  // Default to "dashboard" if no section is provided
  if (!section) section = "dashboard";

  // Update the menu highlight and the URL hash (e.g. #dashboard)
  setActiveMenu(section);
  window.location.hash = section; 


  // Build the API URL for the requested section
  const endpoint = `/section/${section}`;

  try {

    // Fetch the HTML for this section from Flask (e.g. GET /section/budget)
    // Flask renders the Jinja template with real data and sends back plain HTML
    // That HTML is then injected into <div id="section-container"> in index.html
    const response = await fetch(endpoint); 
    // If the server returned an error status (e.g. 404, 500), throw an error
    if (!response.ok) throw new Error("Fetch failed");
    // Read the response body as plain HTML text
    const html = await response.text();
    // Inject the fetched HTML into the section container
    sectionContainer.innerHTML = html;

    // After loading the HTML, we need to run some JavaScript to make it interactive.
    // Each section has its own init function that sets up event listeners and dynamic behavior.
    if (section === "dashboard") loadDashboardChart();
    if (section === "budget") initBudget();
    if (section === "transactions") initTransactions();
    if (section === "goals") initGoals();
    if (section === "settings") initSettings();

  } catch (error) {
    // Something went wrong — show a friendly error message
    console.error("Error loading section:", error);
    sectionContainer.innerHTML = "<p>Unable to load content. Please refresh the page.</p>";
  }
}


// APP INITIALISER

// Sets up event listeners and loads the first section.
// Called once the page has fully loaded.
function initApp() {
  // Attach a click listener to every menu item
  document.querySelectorAll(".menu-item").forEach(link => {
    link.addEventListener("click", event => {
      // Prevent the browser from following the link normally
      event.preventDefault();
      // Load whichever section this menu item points to
      loadSection(link.dataset.section);
    });
  });

  // On first load, read the section from the URL hash (e.g. example.com/#settings)
  // and fall back to "dashboard" if there is no hash
  const initialSection = window.location.hash.replace("#", "") || "dashboard";
  loadSection(initialSection);

  // If the user navigates back/forward in the browser,
  // reload the section that matches the new URL hash
  window.addEventListener("hashchange", () => {
    const section = window.location.hash.replace("#", ""); 
    loadSection(section);
  });
}


// ENTRY POINT
// Wait for the HTML to be fully parsed before running initApp
document.addEventListener("DOMContentLoaded", initApp);

// DOMContentLoaded is an event that 
// fires when the HTML document has been fully loaded and parsed.