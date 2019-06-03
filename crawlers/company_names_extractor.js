rows = document.querySelectorAll('#marketwatchtable tr.linedlist');
companies = []
last = []
for (var i=0; i<rows.length; i++) {
    companies.push(rows[i].childNodes[0].innerText);
}

str = ""
for (var j=0; j<companies.length; j++) {
    str = str + "'" + companies[j] + "', ";    
}