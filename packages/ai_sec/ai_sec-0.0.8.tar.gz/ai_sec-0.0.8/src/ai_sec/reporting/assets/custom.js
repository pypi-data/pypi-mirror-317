// document.addEventListener('DOMContentLoaded', function() {
//     // Function to adjust table container height based on the viewport
//     function adjustTableContainerHeight() {
//         const tableContainer = document.querySelector('.dt-table-container');
//         const cellTable = document.querySelector('.cell-table');
//         const headerHeight = 80; // Estimate for header height or navbar, adjust as needed
//         const footerHeight = 60; // Adjust based on actual footer height

//         if (tableContainer && cellTable) {
//             // Calculate available height and apply it
//             const viewportHeight = window.innerHeight;
//             const availableHeight = viewportHeight - headerHeight - footerHeight;

//             // Apply available height to container and scroll height for the table
//             tableContainer.style.maxHeight = `${availableHeight}px`;
//             cellTable.style.maxHeight = `${availableHeight}px`; // Allow scrolling within this element
//         }
//     }

//     // Run the adjustment function when the page loads and on resize
//     adjustTableContainerHeight();
//     window.addEventListener('resize', adjustTableContainerHeight);
    
//     // Optional: Adjust height on scroll if layout shifts
//     window.addEventListener('scroll', adjustTableContainerHeight);
// });