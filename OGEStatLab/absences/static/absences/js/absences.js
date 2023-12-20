function fetchFilteredAbsences(filterType, filterValue) {
	fetch(`/absences/get_all_absences?filterType=${filterType}&filterValue=${filterValue}`, {
		method: 'GET',
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
		}
	})
	.then(response => response.json())
	.then(data => {
		if (data.error) {
			console.error(data.error);
		} else {
			updateAbsencesList(data.absences);
		}
	})
	.catch(error => console.error('Error:', error));
}

function updateAbsencesList(absences) {
	var table = document.getElementById('absencesTable');
	var tableRows = table.getElementsByTagName('tr');
	var rowCount = tableRows.length;

	// Supprimer les anciennes lignes (à part l'entête)
	for (var x = rowCount - 1; x > 0; x--) {
		table.deleteRow(x);
	}

	// Ajouter les nouvelles lignes
	absences.forEach(function(absence) {
		var row = table.insertRow();
		// Ajouter les cellules pour chaque propriété de l'absence
		row.insertCell(0).innerHTML = absence.subject;
		row.insertCell(1).innerHTML = absence.subjectType;
		row.insertCell(2).innerHTML = absence.classroom;
		row.insertCell(3).innerHTML = absence.teacher;
		row.insertCell(4).innerHTML = formatDateTime(absence.start_date);
		row.insertCell(5).innerHTML = formatDateTime(absence.end_date);
		row.insertCell(6).innerHTML = absence.justification;
	});
}

function formatDateTime(dateTimeStr) {
	var date = new Date(dateTimeStr);
	return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function loadOptions(url, selectId) {
	fetch(url)
	.then(response => response.json())
	.then(data => {
		if (data.error) {
			console.error(data.error);
		} else {
			const select = document.getElementById(selectId);
			Object.values(data)[0].forEach(item => {
				const option = document.createElement('option');
				option.value = item;
				option.textContent = item;
				select.appendChild(option);
			});
		}
	})
	.catch(error => console.error('Error:', error));
}

document.getElementById('teacherFilter').addEventListener('change', function() {
	fetchFilteredAbsences('teacher', this.value);
});

document.getElementById('subjectTypeFilter').addEventListener('change', function() {
	fetchFilteredAbsences('subjectType', this.value);
});

document.getElementById('classroomFilter').addEventListener('change', function() {
	fetchFilteredAbsences('classroom', this.value);
});

loadOptions('/absences/get_all_classrooms/', 'classroomFilter');
loadOptions('/absences/get_all_teachers/', 'teacherFilter');

// Chargez initialement toutes les absences
fetchFilteredAbsences(null, null);
