function rowToCSV(row) {
    let csv_row = '';
    for (let i = 0; i < row.length - 1; i++) {
	csv_row += row[i] + ',';
    }
    csv_row += row[row.length - 1] + '\n';

    return csv_row;
}


document.addEventListener('DOMContentLoaded', function() {
    // test results to csv file
    document.getElementById('to-csv').addEventListener('click', function() {
	let results = [
	    ['uživatel', 'počet bodů']
	];

	let names = document.getElementsByClassName('name');
	let scores = document.getElementsByClassName('score');

	// collecting data array
	for (let i = 0; i < scores.length; i++) {
	    results.push([
		names[i].innerHTML,
		scores[i].innerHTML
	    ]);
	}

	// creating csv
	let csv = '';

	for (let i = 0; i < results.length; i++) {
	    csv += rowToCSV(results[i]);
	}

	// downloading
	let anchor = document.createElement('A');
	anchor.download = document.querySelector('H1').innerHTML + '.csv';

	let blob = new Blob([csv], {type: 'text/csv'});
	anchor.href = URL.createObjectURL(blob);

	anchor.click();
    });
});
