async function getCurriculum(live = false) {
	const username = localStorage.getItem("username");
	const curriculum = (await post("/chaoxing/get_curriculum",
				       live)).json();
	if (username != localStorage.getItem("username"))
		return;
	const e = document.getElementById("curriculum-list-div");
	const d = newElement("div");
	e.replaceChildren(d);
	if (!Object.keys(curriculum).length) {
		d.innerText = "Error fetching curriculum.";
		return;
	}
	d.innerText = `Current year ${curriculum.details.year}, ` +
		      `semester ${curriculum.details.semester}, ` +
		      `week ${curriculum.details.week}.`;
	if (!Object.keys(curriculum.lessons).length) {
		d.innerText += " No curriculum.";
		return;
	}
	const table = newElement("table", {"style": "border = 1"});
	const tb = table.appendChild(newElement("tbody"));
	const timetable = curriculum.details.time.timetable;
	for (let lesson of Object.values(curriculum.lessons)) {
		const tr = tb.appendChild(newElement("tr"));
		let td = tr.appendChild(newElement("td"));
		td.appendChild(document.createTextNode(lesson.name));
		td = tr.appendChild(newElement("td"));
		lesson.teachers.forEach((v, i) => {
			if (i)
				td.appendChild(newElement("br"));
			td.appendChild(document.createTextNode(v));
		});
		td = tr.appendChild(newElement("td"));
		lesson.times.forEach((v, i) => {
			if (i)
				td.appendChild(newElement("br"));
			const bgn = timetable[v.period_begin - 1].slice(0, 5);
			const end = timetable[v.period_end - 1].slice(6, 11);
			td.appendChild(document.createTextNode(`${v.day}  ` +
							      `${bgn}-${end}`));

		});
		td = tr.appendChild(newElement("td"));
		if (lesson.livestreams) {
			lesson.livestreams.forEach((v, i) => {
				if (i)
					td.appendChild(newElement("br"));
				td.appendChild(newElement("button", {
					innerText: v.classroom, onclick:
					() => setClassroom(v.url, v.classroom)
				}));
			});
			continue;
		}
		lesson.classrooms.forEach((v, i) => {
			if (i)
				td.appendChild(newElement("br"));
			const url = getClassroomUrl(v);
			td.appendChild(url ? newElement("button", {
				innerText: v,
				onclick: () => setClassroom(url, v)
			}) : document.createTextNode(v));
		});
	}
	e.appendChild(table);
}
