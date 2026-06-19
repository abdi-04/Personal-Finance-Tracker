let allTransactions = []; // Store all transactions globally so other functions can access them
let dashboardChart; // Store the chart so we can destroy and recreate it later
let canvas; // Store the canvas element so other functions can use it

// LOAD DATA

async function loadDashboardChart() { 
    canvas = document.getElementById("incomeExpenseChart"); // Find the chart canvas element in the HTML
    if (!canvas) return; // If the canvas doesn't exist, stop the function early

    try { 
        const response = await fetch("/transactions"); // Ask the server for all transactions and wait for a response
        if (!response.ok) throw new Error("Could not load transactions"); // If the server returned an error, stop and throw an error

        const data = await response.json(); // Convert the response into a JavaScript object and wait for it
        allTransactions = data.transactions || []; // Save the transactions, or use an empty array if there are none

        const years = populateYearSelect(allTransactions); // Fill the year dropdown with available years and get the list back

        const latestYear = Math.max(...years); // Find the most recent year from the list
        document.getElementById("yearSelect").value = latestYear; // Set the dropdown to show the most recent year

        filterAndBuild(latestYear); // Build the chart using only the most recent year's transactions

    } catch (error) { // If anything in the try block went wrong, run this
        console.error("Dashboard chart error:", error); // Print the error to the browser console
    }
}


// GET YEARS FROM DATA

function getYears(transactions) { // Takes the full list of transactions as input
    const years = transactions.map(t => { // Loop through every transaction and transform it
        return new Date(t.date).getFullYear(); // Convert the transaction's date to just a 4-digit year
    });

    return [...new Set(years)].sort((a, b) => a - b); // Remove duplicate years, convert to array, and sort oldest to newest
}


// POPULATE DROPDOWN

function populateYearSelect(transactions) { // Takes transactions and fills the year dropdown in the HTML
    const select = document.getElementById("yearSelect"); // Find the dropdown element in the HTML
    const years = getYears(transactions); // Get the sorted list of unique years from the transactions

    select.innerHTML = ""; // Clear the dropdown in case it already has options in it

    years.forEach(year => { // Loop through each year
        const option = document.createElement("option"); // Create a new dropdown option element
        option.value = year; // Set the option's value to the year number
        option.textContent = year; // Set the text the user sees in the dropdown to the year number
        select.appendChild(option); // Add the option to the dropdown
    });

    select.addEventListener("change", (event) => { // Listen for when the user picks a different year
        const year = Number(event.target.value); // Get the selected year and convert it from a string to a number
        filterAndBuild(year); // Rebuild the chart using the newly selected year
    });

    return years; // Send the years list back to whoever called this function
}


// FILTER + BUILD CHART

function filterAndBuild(year) { // Takes a year and filters transactions down to just that year
    const filtered = allTransactions.filter(trans => { // Loop through all transactions and keep only matching ones
        return new Date(trans.date).getFullYear() === year; // Keep the transaction if its year matches the selected year
    });

    buildChart(filtered, canvas); // Build the chart using only the filtered transactions
}


// BUILD CHART

function buildChart(transactions, canvas) { // Takes a list of transactions and a canvas element to draw on

    const months = [ // Array of month name labels for the chart's x-axis
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sept","Oct","Nov","Dec"
    ];

    const monthly = Array.from({ length: 12 }, () => ({ // Create an array of 12 objects, one for each month
        income: 0, // Each month starts with zero income
        expenses: 0 // Each month starts with zero expenses
    }));

    transactions.forEach(trans => { // Loop through every transaction
        const date = new Date(trans.date); // Convert the transaction's date string into a Date object
        const m = date.getMonth(); // Get the month number (0 = January, 11 = December)

        if (trans.type === "income") { // If this transaction is income
            monthly[m].income += Number(trans.amount); // Add the amount to that month's income total
        } 
        else { // Otherwise treat it as an expense
            monthly[m].expenses += Number(trans.amount); // Add the amount to that month's expenses total
        }
    });

    const incomeData   = monthly.map(m => m.income); // Extract just the income value from each month into an array
    const expensesData = monthly.map(m => m.expenses); // Extract just the expenses value from each month into an array
    const netData      = monthly.map(m => m.income - m.expenses); // Calculate net (income minus expenses) for each month

    if (dashboardChart instanceof Chart) { // Check if a chart already exists
        dashboardChart.destroy(); // If so, destroy it before drawing a new one to avoid overlap
    }

    dashboardChart = new Chart(canvas, { // Create a new Chart.js chart and save it to dashboardChart
        type: "line", // Use a line chart
        data: {
            labels: months, // Use the month names as x-axis labels
            datasets: [
                {
                    label: "Income", // Name shown in the legend
                    data: incomeData, // The income values to plot
                    borderColor: "rgba(34, 197, 94, 1)", // Green line color
                    tension: 0.4, // Makes the line curved instead of sharp
                    fill: true, // Fill the area under the line
                    pointRadius: 5 // Size of the dots on the line
                },
                {
                    label: "Expenses", // Name shown in the legend
                    data: expensesData, // The expenses values to plot
                    borderColor: "rgba(239, 68, 68, 1)", // Red line color
                    tension: 0.4, // Makes the line curved instead of sharp
                    fill: true, // Fill the area under the line
                    pointRadius: 5 // Size of the dots on the line
                },
                {
                    label: "Net", // Name shown in the legend
                    data: netData, // The net values to plot
                    borderColor: "rgba(99, 102, 241, 1)", // Purple line color
                    tension: 0.4, // Makes the line curved instead of sharp
                    fill: true, // Fill the area under the line
                    pointRadius: 5 // Size of the dots on the line
                }
            ]
        },
        options: {
            plugins: {
                legend: { // Settings for the chart legend
                    labels: {
                        usePointStyle: true, // Use a shape instead of a rectangle in the legend
                        pointStyle: "circle" // Make that shape a circle
                    }
                }
            }
        }
    });
}


