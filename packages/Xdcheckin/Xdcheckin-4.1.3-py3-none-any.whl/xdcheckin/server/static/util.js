function assert(cond, msg) {
	if (!cond)
		throw new Error(msg || "Assertion failed.");
}

function isValidUrl(url) {
	try {
		new URL(url);
		return true;
	} catch (err) {
		return false;
	}
}

async function post(url = "", data = {}) {
	let status = 404, text = "";
	try {
		const res = await fetch(url, {
			method: "POST", credentials: "include",
			body: JSON.stringify(data)
		});
		status = res.status;
		text = await res.text();
	}
	catch (err) {}
	return {
		status, text, json: () => {
			try {
				return JSON.parse(text);
			} catch (err) {
				return {};
			}
		}
	};
}

function newElement(tag, properties = {}) {
	const e = (typeof tag != "object") ? document.createElement(tag) : tag;
	return Object.assign(e, properties);
}

async function displayTag(e_id, display) {
	const e = document.getElementById(e_id);
	if (display === undefined)
		e.style.display = e.style.display == "none" ? "" : "none";
	else
		e.style.display = display ? "" : "none";
}

async function hideOtherLists(e_id) {
	const e_ids = [
		"accounts-list-div", "curriculum-list-div",
		"locations-list-div", "activities-list-div",
		"classrooms-list-div"
	];
	for (let id of e_ids)
		if (id != e_id)
			document.getElementById(id).style.display = "none";
	if (e_id)
		displayTag(e_id);
}

function unescapeUnicode(s) {
	return s.replace(/\\u[\dA-Fa-f]{4}/g, match =>
			 String.fromCharCode(parseInt(match.substring(2), 16)));
}

async function screenshot_scan(video) {
	await zbarWasmReady;
	if (video.readyState < video.HAVE_ENOUGH_DATA)
		return [];
	const canvas = newElement("canvas");
	canvas.height = video.videoHeight;
	canvas.width = video.videoWidth;
	const ctx = canvas.getContext("2d");
	ctx.drawImage(video, 0, 0);
	const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
	return (await zbarWasm.scanImageData(data)).map(s => s.decode());
}

function dumpsDebugInfo() {
	const d = {};
	for (let i = 0; i < localStorage.length; ++i) {
		const k = localStorage.key(i);
		if (!/aliplayer/.test(k))
			d[k] = localStorage.getItem(k);
	}
	for (let k of [
		"accounts", "password", "cookie", "location_", "classroom",
		"opacity", "color", "darkMode"
	])
		delete d[k];
	const c = JSON.parse(localStorage.getItem("cookies") || "{}");
	for (let k of [
		"uf", "_d", "vc", "vc2", "vc3", "cx_p_token", "p_auth_token",
		"xxtenc", "route", "_industry", "lv", "fidsCount",
		"KI4SO_SERVER_EC", "DSSTASH_LOG", "JSESSIONID"
	])
		delete c[k];
	d["cookies"] = c;
	d["chaoxing_config"] = JSON.parse(JSON.parse(localStorage.getItem(
				   "accounts"))[d["username"]].chaoxing_config);
	d["g_courses_keys_length"] = Object.keys(globalThis.g_courses).length;
	d["classroom_length"] = localStorage.getItem("classroom").length;
	d["location_"] = JSON.parse(localStorage.getItem("location_"));
	return JSON.stringify(d);
}

async function checkEula() {
	const msg = "This APP provides utilities for Chaoxing check-ins " +
		  "and classroom livestreams exclusively for XDUers.\n\n" +
		  "By confirming you agree to the following terms:\n" +
		  "    1. This APP is for study use only.\n" +
		  "    2. This work comes with absolutely no warranty.\n\n" +
		  "You have been warned.";
	if (!localStorage.getItem("xdcheckin_eula"))
		if (confirm(msg))
			localStorage.setItem("xdcheckin_eula", "1");
		else
			document.getElementById("main-body").style.display =
									 "none";
}

async function xdcheckinCheckUpdates() {
	const ver = (await post("/xdcheckin/get_version")).text;
	document.getElementById("footer-link-a").innerText += ` ${ver}`;
	const update = (await post("/xdcheckin/get_update")).json();
	if (update && update.updatable)
		document.getElementById("xdcheckin-update-div").innerHTML =
			`<a href='${update.html_url}'>` +
			`Version ${update.tag_name} released.` +
			`</a><br>${update.body.replaceAll('\r\n', '<br>')}`;
}
