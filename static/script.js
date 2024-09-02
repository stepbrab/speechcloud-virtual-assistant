    // dialogue_paused = true

    // Globalni promenna pro ukladani data
    var events = [];
    var shop = [];

    var message_already_sent_flag = false

    // SIP session, tj. hovor
    var session;

    // Výchozí URI, odkud se stáhne konfigurace ASR+TTS
    var SPEECHCLOUD_URI = "https://"+window.location.host.replace("444", "443")+"/v1/speechcloud/";
    var SPEECHCLOUD_DEFAULT_APP_ID = "numbers";

    // Proměnná pro udržení odkazu na řídící WebSocket
    var SPEECHCLOUD_WS = null;

    /* Výběr prvků z pole */
    function choose(choices) {
        var index = Math.floor(Math.random() * choices.length); return choices[index];
    }

    /* Logovací funkce */
    function hlog(text) {
        $("#log").prepend("<div>"+text+"<br/></div>");
    }

    $( document ).ready(function() {
        const themeColors = [
            '#3f51b5',
            '#2E7D32',
            '#6A1B9A',
            '#1565C0',
            '#283593',
            '#4E342E',
            '#37474F',
            '#6b0b09',
            '#000000'
        ];
        let currentColorIndex = 0;

        function changeThemeColor() {
            currentColorIndex = (currentColorIndex + 1) % themeColors.length;
            const newColor = themeColors[currentColorIndex];
            
            document.documentElement.style.setProperty('--theme-color', newColor);
        }

        document.addEventListener('keydown', function(event) {
            if (event.altKey && event.key === 't') {
                event.preventDefault();
                changeThemeColor();
            }
        });
        
        // Chat
        function addChatMessage(message, isIncoming) {
            const chatMessages = document.getElementById('chat-messages');
            const messageElement = document.createElement('div');
            messageElement.classList.add('chat-message');
            messageElement.classList.add(isIncoming ? 'incoming' : 'outgoing');
            messageElement.textContent = message;
            
            const wrapperDiv = document.createElement('div');
            wrapperDiv.style.width = '100%';
            wrapperDiv.style.display = 'flex';
            wrapperDiv.style.justifyContent = isIncoming ? 'flex-start' : 'flex-end';
            
            wrapperDiv.appendChild(messageElement);
            chatMessages.appendChild(wrapperDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        document.getElementById('chat-send-button').addEventListener('click', function() {
            const input = document.getElementById('chat-text-input');
            const message = input.value.trim();
            if (message) {
                addChatMessage(message, false);
                message_already_sent_flag = true
                input.value = '';
                speechCloud.asr_process_text({text: message});
            }
        });

        document.getElementById('chat-text-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('chat-send-button').click();
            }
        });

        // Popup windows
        const POLOZKA = {
            "pečivo": {},
            "šunka": {},
            "sýr": {},
            "těstoviny": {},
            "rýže": {},
            "brambory": {},
            "kuřecí maso": {},
            "vepřové maso": {},
            "hovězí maso": {},
            "mleté maso": {},
            "ovesné vločky": {},
            "cereálie": {},
            "mléko": {},
            "vejce": {},
            "chléb": {},
            "máslo": {},
            "olej": {},
            "jogurt": {},
            "banán": {},
            "jablko": {},
            "hruška": {},
            "pomeranč": {},
            "citron": {},
            "okurka": {},
            "rajče": {},
            "paprika": {},
            "salát": {},
            "brokolice": {},
            "květák": {},
            "cuketa": {},
            "mrkev": {},
            "cibule": {},
            "česnek": {},
            "chilli": {},
            "rohlík": {},
            "sušený salám": {},
            "slanina": {},
            "klobása": {},
            "anglická slanina": {},
            "smetana": {},
            "tvaroh": {},
            "zmrzlina": {},
            "mouka": {},
            "cukr": {},
            "sůl": {},
            "pepř": {},
            "kmín": {},
            "kečup": {},
            "hořčice": {},
            "majonéza": {},
            "ocet": {},
            "med": {},
            "džem": {},
            "povidla": {},
            "čokoláda": {},
            "minerálka": {},
            "limonáda": {},
            "pivo": {},
            "víno": {},
            "rum": {},
            "whisky": {},
            "vodka": {},
            "zelí": {},
            "špenát": {},
            "hrách": {},
            "čočka": {},
            "fazole": {},
            "krůtí maso": {},
            "jehněčí maso": {},
            "ryba": {},
            "losos": {},
            "tuňák": {},
            "kapr": {},
            "ořechy": {},
            "mandle": {},
            "rozinky": {},
            "kuskus": {},
            "bulgur": {},
            "quinoa": {},
            "tofu": {},
            "tempeh": {},
            "sójové maso": {},
            "granola": {},
            "müsli": {},
            "pudink": {},
            "želatina": {},
            "droždí": {},
            "prášek do pečiva": {},
            "vanilkový cukr": {},
            "skořice": {},
            "zázvor": {},
            "kurkuma": {},
            "oregano": {},
            "bazalka": {},
            "tymián": {},
            "rozmarýn": {},
            "bobkový list": {},
            "nové koření": {},
            "hřebíček": {},
            "kardamom": {}
        };

        const AKCE = {
            "schůzka": {},
            "obecná událost": {},
            "návštěva doktora": {},
            "oběd": {},
            "rezervace": {},
            "večeře": {},
            "telefonát": {},
            "osobní úkol": {},
            "přednáška": {},
            "konference": {},
            "výlet": {},
            "narozeniny": {},
            "trénink": {},
            "zkouška": {},
            "porada": {},
            "setkání s přáteli": {},
            "rodinná událost": {},
            "mentoring": {}
        };

        function populateDatalist(datalistId, items) {
            const datalist = document.getElementById(datalistId);
            for (const key in items) {
                const option = document.createElement('option');
                option.value = key;
                datalist.appendChild(option);
            }
        }
        
        let isEventDeleteMode = false;
        let isShoppingDeleteMode = false;

        document.getElementById('add-event').addEventListener('click', showAddEventPopup);
        document.getElementById('delete-event').addEventListener('click', toggleEventDeleteMode);
        document.getElementById('add-item').addEventListener('click', showAddItemPopup);
        document.getElementById('delete-item').addEventListener('click', toggleShoppingDeleteMode);

        function showPopup(content) {
            const overlay = document.createElement('div');
            overlay.className = 'popup-overlay';
            document.body.appendChild(overlay);

            const popup = document.createElement('div');
            popup.className = 'popup';
            popup.innerHTML = content;
            document.body.appendChild(popup);

            overlay.style.display = 'block';
            popup.style.display = 'block';

            return { popup, overlay };
        }

        function closePopup(popup, overlay) {
            popup.remove();
            overlay.remove();
        }

        function showAddEventPopup() {
            const { popup, overlay } = showPopup(`
                <h3>Přidat událost</h3>
                <input type="text" id="event-name" list="event-names" placeholder="Typ" required>
                <datalist id="event-names">
                    <!-- Event names will be populated here -->
                </datalist>
                <input type="date" id="event-date" required>
                <input type="time" id="event-start-time" min="06:00" max="20:00" step="1800" required>
                <input type="time" id="event-end-time" min="06:00" max="20:00" step="1800" required>
                <div class="popup-buttons">
                    <button id="add-event-btn">Přidat</button>
                    <button class="cancel">Zrušit</button>
                </div>
            `);

            populateDatalist('event-names', AKCE);

            popup.querySelector('.cancel').addEventListener('click', () => closePopup(popup, overlay));
            popup.querySelector('#add-event-btn').addEventListener('click', () => {
                const name = document.getElementById('event-name').value;
                let startTime = document.getElementById('event-start-time').value;
                let endTime = document.getElementById('event-end-time').value;
                const date = document.getElementById('event-date').value;

                if (!name || !date || !startTime || !endTime) {
                    alert('Prosím vyplňte všechna pole.');
                    return;
                }
                if (!AKCE.hasOwnProperty(name)) {
                    alert('Prosím vyberte validní typ události.');
                    return;
                }
                if (startTime >= endTime) {
                    alert('Čas začátku musí být dříve, než čas konce události.');
                    return;
                }
                let [hours, minutes] = startTime.split(':');
                if (hours < 6 || hours > 20) {
                    alert('Prosím zadejte validní čas.\nČas musí být v rozmezí 06:00 - 20:00.');
                    return;
                }
                if (minutes != 30 && minutes != 0) {
                    alert('Prosím zadejte validní čas.\nČas musí být v půlhodinových inkrementech.')
                    return;
                }
                [hours, minutes] = endTime.split(':');
                if (hours < 6 || hours > 20) {
                    alert('Prosím zadejte validní čas.\nČas musí být v rozmezí 06:00 - 20:00.');
                    return;
                }
                if (minutes != 30 && minutes != 0) {
                    alert('Prosím zadejte validní čas.\nČas musí být v půlhodinových inkrementech.')
                    return;
                }

                if (startTime.slice(0,1) == '0') {
                    startTime = startTime.slice(1);
                }

                if (endTime.slice(0,1) == '0') {
                    endTime = endTime.slice(1);
                }

                let [year, month, day] = date.split('-');

                if (month.slice(0,1) == '0') {
                    month = month.slice(1);
                }

                if (day.slice(0,1) == '0') {
                    day = day.slice(1);
                }

                const newEvent = {
                    type: name,
                    date_day: day + '.',
                    date_month: month + '.',
                    date_year: year,
                    time_start: startTime,
                    time_end: endTime
                };

                events.push(newEvent);
                populateEvents(events);
                syncWithServer();
                popup.remove();
                closePopup(popup, overlay);
            });
        }

        function showAddItemPopup() {
            const { popup, overlay } = showPopup(`
                <h3>Přidat položku</h3>
                <input type="text" id="item-name" list="item-names" placeholder="Název" required>
                <datalist id="item-names">
                    <!-- Item names will be populated here -->
                </datalist>
                <input type="number" id="item-quantity" min="1" value="1" required>
                <div class="popup-buttons">
                    <button id="add-item-btn">Přidat</button>
                    <button class="cancel">Zrušit</button>
                </div>
            `);

            populateDatalist('item-names', POLOZKA);

            popup.querySelector('.cancel').addEventListener('click', () => closePopup(popup, overlay));
            popup.querySelector('#add-item-btn').addEventListener('click', () => {
                const name = document.getElementById('item-name').value;
                const quantity = parseInt(document.getElementById('item-quantity').value);

                if (!quantity || !name) {
                    alert('Prosím vyplňte všechna pole.');
                    return;
                }
                if (!POLOZKA.hasOwnProperty(name)) {
                    alert('Prosím vyberte validní položku.');
                    return;
                }

                if (quantity < 1) {
                    alert('Množství musí být rovno alespoň 1.');
                    return;
                }

                const existingItemIndex = shop.findIndex(item => item.name === name);

                if (existingItemIndex !== -1) {
                    shop[existingItemIndex].amount += quantity;
                } else {
                    const newItem = {
                        name: name,
                        amount: quantity
                    };
                    shop.push(newItem);
                }

                populateShoppingList(shop);
                syncWithServer();
                closePopup(popup, overlay);
            });
        }

        // Delete buttons
        function toggleEventDeleteMode() {
            isEventDeleteMode = !isEventDeleteMode;
            const deleteButton = document.getElementById('delete-event');
            deleteButton.classList.toggle('active', isEventDeleteMode);
            populateEvents(events);
        }

        function toggleShoppingDeleteMode() {
            isShoppingDeleteMode = !isShoppingDeleteMode;
            const deleteButton = document.getElementById('delete-item');
            deleteButton.classList.toggle('active', isShoppingDeleteMode);
            populateShoppingList(shop);
        }

        function showConfirmationPopup(message, onConfirm) {
            const { popup, overlay } = showPopup(`
                <h3>Potvrzení odstranění</h3>
                <p>${message}</p>
                <div class="popup-buttons">
                    <button id="confirm-delete">Odstranit</button>
                    <button class="cancel">Zrušit</button>
                </div>
            `);

            popup.querySelector('.cancel').addEventListener('click', () => closePopup(popup, overlay));
            popup.querySelector('#confirm-delete').addEventListener('click', () => {
                onConfirm();
                closePopup(popup, overlay);
            });
        }

        function deleteEvent(index) {
            showConfirmationPopup('Opravdu si přejete odstranit danou událost?', () => {
                events.splice(index, 1);
                populateEvents(events);
                syncWithServer();
            });
        }

        function deleteShoppingItem(index) {
            showConfirmationPopup('Opravdu si přejete odstranit danou položku?', () => {
                shop.splice(index, 1);
                populateShoppingList(shop);
                syncWithServer();
            });
        }

        // Synchronizace se serverem
        function syncWithServer() {
            const data = {
                events: events,
                shopping_lists: [{
                    items: shop
                }]
            };
            speechCloud.dm_send_message({data: JSON.stringify(data)});
        }

        const calendarContainer = document.getElementById('calendar-container');
        const today = new Date();
        const defaultDayIndex = today.getDay();
        const dayIndex = defaultDayIndex === 0 ? 6 : defaultDayIndex-1; // sunday is 0... make it 6 and monday 0 as we are european

        let currentWeekStart = new Date(today.setDate(today.getDate() - dayIndex));
        

        const daysOfWeek = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'];

        // Nadchazejici udalost
        function updateUpcomingEvent() {
            const now = new Date();
            let closestEvent = null;
            let closestEventData = null;
            console.log('now', now)
            for (let event of events) {
                let [hour, minute] = event.time_start.split(':');
                hour = hour.padStart(2, '0');
                const formattedTimeStart = `${hour}:${minute}`;

                const eventDate = new Date(
                    `${event.date_year}-${event.date_month.slice(0, -1).padStart(2, '0')}-${event.date_day.slice(0, -1).padStart(2, '0')}T${formattedTimeStart}`
                );
                console.log('upcm', eventDate)

                if (eventDate > now && (!closestEvent || eventDate < closestEvent)) {
                    closestEvent = eventDate;
                    console.log(closestEvent)
                    closestEventData = event;
                }
            }

            const upcomingEventDetails = document.getElementById('upcoming-event-details');

            if (closestEventData) {
                upcomingEventDetails.innerHTML = `
                    <p><strong>Typ:</strong> ${closestEventData.type}</p>
                    <p><strong>Datum:</strong> ${closestEventData.date_day.slice(0, -1)}.${closestEventData.date_month.slice(0, -1)}.${closestEventData.date_year}</p>
                    <p><strong>Čas:</strong> ${closestEventData.time_start} - ${closestEventData.time_end}</p>
                `;
            } else {
                upcomingEventDetails.innerHTML = '<p>Žádné nadcházející události</p>';
            }
        }

        // Indikator casu v kalendari
        function updateCurrentTimeIndicator() {
            const now = new Date();
            const currentHour = now.getHours();
            const currentMinute = now.getMinutes();
            const dateString = now.toISOString().split('T')[0]; // format as YYYY-MM-DD

            if (currentHour >= 6 && currentHour < 20) {
                const dayCell = document.querySelector(`.day[data-date="${dateString}"][data-hour="${currentHour}"]`);

                if (dayCell) {
                    const existingIndicator = document.querySelector('.current-time-indicator');
                    if (existingIndicator) {
                        existingIndicator.remove();
                    }

                    const indicator = document.createElement('div');
                    indicator.className = 'current-time-indicator';
                    const topPercentage = (currentMinute / 60) * 100;
                    indicator.style.cssText = `
                        position: absolute;
                        left: 0;
                        right: 0;
                        top: ${topPercentage}%;
                        height: 2px;
                        background-color: black;
                        z-index: 10;
                    `;
                    dayCell.appendChild(indicator);
                }
            }
        }
        
        // Generace kalendare
        function generateCalendar(weekStart) {
            let calendar = '<div class="hour"></div>'; 

            // Add day headers
            for (let day = 0; day < 7; day++) {
                const currentDate = new Date(weekStart.getFullYear(), weekStart.getMonth(), weekStart.getDate() + day);
                calendar += `<div class="day-header">${daysOfWeek[day]}<br>${currentDate.toLocaleDateString('cs-CZ', { day: 'numeric', month: 'numeric' })}</div>`;
            }

            // Add hourly rows
            for (let hour = 6; hour < 20; hour++) {
                calendar += `<div class="hour">${hour.toString().padStart(2, '0')}:00</div>`;
                for (let day = 0; day < 7; day++) {
                    const currentDate = new Date(weekStart.getFullYear(), weekStart.getMonth(), weekStart.getDate() + day + 1);
                    const dateString = currentDate.toISOString().split('T')[0]; 
                    calendar += `<div class="day" data-date="${dateString}" data-hour="${hour}"></div>`;
                }
            }

            document.getElementById('calendar').innerHTML = calendar;
            updateCurrentWeekDisplay(weekStart);
            
            document.querySelectorAll('.event').forEach(el => el.remove());
            
            populateEvents(events);

            updateUpcomingEvent();
            updateCurrentTimeIndicator();
        }

        // Navigace v tydnech v kalendari
        function updateCurrentWeekDisplay(weekStart) {
            const weekEnd = new Date(weekStart.getFullYear(), weekStart.getMonth(), weekStart.getDate() + 6);
            const formatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
            const weekStartStr = weekStart.toLocaleDateString('cs-CZ', formatOptions);
            const weekEndStr = weekEnd.toLocaleDateString('cs-CZ', formatOptions);
            document.getElementById('current-week').textContent = `${weekStartStr} - ${weekEndStr}`;
        }

        setInterval(updateUpcomingEvent, 60000);
        setInterval(updateCurrentTimeIndicator, 60000); 

        function populateEvents(events) {
            document.querySelectorAll('.event').forEach(el => el.remove());

            events.forEach((event, index) => {
                const eventDate = new Date(`${event.date_year}-${event.date_month.slice(0, -1).padStart(2, '0')}-${event.date_day.slice(0, -1).padStart(2, '0')}`);
                const eventStartHour = parseInt(event.time_start.split(':')[0], 10);
                console.log('minuty', parseInt(event.time_end.split(':')[1], 10));
                let eventEndHour;
                if (parseInt(event.time_end.split(':')[1], 10) == 30){
                    eventEndHour = parseInt(event.time_end.split(':')[0], 10) + 1;
                }
                else{
                    eventEndHour = parseInt(event.time_end.split(':')[0], 10);
                };
                
                const dateString = eventDate.toISOString().split('T')[0]; 
                const eventCategory = categorizeEvent(event.type);

                for (let hour = eventStartHour; hour < eventEndHour; hour++) {
                    const cell = document.querySelector(`.day[data-date="${dateString}"][data-hour="${hour}"]`);
                    if (cell) {
                        const eventElement = document.createElement('div');
                        eventElement.className = `event ${eventCategory}`;
                        eventElement.title = `${event.type} (${event.time_start} - ${event.time_end})`;
                        eventElement.textContent = event.type;

                        if (isEventDeleteMode) {
                            eventElement.classList.add('deletable');
                            eventElement.onclick = (e) => {
                                e.stopPropagation();
                                deleteEvent(index);
                            };
                        }

                        cell.appendChild(eventElement);
                    }
                }
            });

            updateUpcomingEvent();
            updateCurrentTimeIndicator();
        }

        // Nacteni udalosti do kalendare
        function populateShoppingList(shop) {
            const listContainer = document.getElementById('shopping-list-container').querySelector('ul');
            listContainer.innerHTML = ''; // Clear previous list

            shop.forEach((item, index) => {
                const li = document.createElement('li');
                li.textContent = `${item.amount}x ${item.name}`;
                
                if (isShoppingDeleteMode) {
                    li.classList.add('deletable');
                    li.onclick = () => deleteShoppingItem(index);
                }
                
                listContainer.appendChild(li);
            });
        }

        generateCalendar(currentWeekStart);
        populateShoppingList(shop);

        document.querySelector('#calendar-container .prev').addEventListener('click', function() {
            currentWeekStart.setDate(currentWeekStart.getDate() - 7);
            generateCalendar(new Date(currentWeekStart));
        });

        document.querySelector('#calendar-container .next').addEventListener('click', function() {
            currentWeekStart.setDate(currentWeekStart.getDate() + 7);
            generateCalendar(new Date(currentWeekStart));
        });

        function categorizeEvent(eventType) {
            const categories = {
                work: ['schůzka', 'telefonát', 'osobní úkol', 'porada', 'mentoring'],
                social: ['setkání s přáteli', 'rodinná událost', 'narozeniny', 'večeře', 'oběd'],
                health: ['návštěva doktora', 'trénink'],
                leisure: ['výlet', 'rezervace'],
                education: ['přednáška', 'konference', 'zkouška'],
            };

            for (const [category, events] of Object.entries(categories)) {
                if (events.includes(eventType)) {
                    return category;
                }
            }

            return 'other';
        }

        function formatTime(date) {
            let hours = date.getHours();
            let minutes = date.getMinutes();
            let seconds = date.getSeconds();
            
            hours = hours < 10 ? '0' + hours : hours;
            minutes = minutes < 10 ? '0' + minutes : minutes;
            seconds = seconds < 10 ? '0' + seconds : seconds;
            
            return `${hours}:${minutes}:${seconds}`;
        }

        function updateTime() {
            const timeElement = document.getElementById('time');
            const now = new Date();
            timeElement.textContent = formatTime(now);
        }

        setInterval(updateTime, 500);

        updateTime();


        // Speechcloud API
        $("#chat-text-input").focus(function () {
            console.log("ignore_space = true");
            ignore_space = true;
        });

        $("#chat-text-input").focusout(function () {
            console.log("ignore_space = false");
            ignore_space = false;
        });

        /* Obsluha tlačítka barge-in*/
        $("#tts_stop").click(do_tts_stop);

        $("#slu_set_nbest_2").click(function () {
            speechCloud.slu_set_nbest({nbest: 2});
        });

        $("#slu_set_nbest_10").click(function () {
            speechCloud.slu_set_nbest({nbest: 10});
        });
        
        $("#slu_test").click(function () {
            speechCloud.slu_set_grammars(
                {"grammars": [
                    {"entity":"ALT", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/ALT.abnf"},
                    {"entity":"CMD", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/CMD.abnf"},
                    {"entity":"CS","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/CS.abnf"},
                    {"entity":"FL","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FL.abnf"},
                    {"entity":"FR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FR.abnf"},
                    {"entity":"HE","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/HE.abnf"},
                    {"entity":"PO","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/PO.abnf"},
                    {"entity":"QNH","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/QNH.abnf"},
                    {"entity":"RA","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/RA.abnf"},
                    {"entity":"SP","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SP.abnf"},
                    {"entity":"SQ","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SQ.abnf"},
                    {"entity":"TU","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TU.abnf"},
                    {"entity":"TWR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TWR.abnf"}
                ]});
        });

        $("#grm_test").click(function () {
            speechCloud.itblp_gen_grammar({"se_type": "CS", "values": ["MTL572", "CSA024", "OKRHH", "AUA123"]});
        });

        $("#asr_set_grammar").click(function () {
            var grammar = "#ESGF V1.0;\n" +
    "grammar prikaz;\n" +
    "public <prikaz>=(zatoč <smer>|jeď <kam>|<vypln>)*;\n" +
    "<smer>=(doleva|doprava);\n" +
    "<kam>=(rovně|dopředu|dozadu);\n" +
    "<vypln>=(a|potom);\n";
            speechCloud.asr_set_grammar({"grammar_type": "esgf", "grammar": grammar});
        });


        // $("#asr_test").click(function () {
        //     speechCloud.asr_test({"words": ["Air_Prague", "Prague_Air"]});
        // });

        $("#process_text").click(function () {
            text = $("#process_text_input").val();
            speechCloud.asr_process_text({text: text});
            $("#process_text_input").val("")
        });

        $("#send_message").click(function () {
            data = JSON.parse($("#send_message_input").val());
            speechCloud.dm_send_message({data: data});
            $("#send_message_input").val("")
        });

        $("#tts_text").click(function () {
            text = $("#process_text_input").val();
            do_tts(text);
            $("#process_text_input").val("")
        });


        var ignore_space = false;

        $("#process_text_input").focus(function () {
            console.log("ignore_space = true");
            ignore_space = true;
        });

        $("#process_text_input").focusout(function () {
            console.log("ignore_space = false");
            ignore_space = false;
        });

        $("#send_message_input").focus(function () {
            console.log("ignore_space = true");
            ignore_space = true;
        });

        $("send_message_input").focusout(function () {
            console.log("ignore_space = false");
            ignore_space = false;
        });



        /* Stavová proměnná a funkce pro spuštění/pozastavení rozpoznávání */
        var recognizing = false;

        function do_recognize() {
            if (!recognizing) {
                speechCloud.asr_recognize();
            };
        }

        function do_pause() {
            if (recognizing) {
                speechCloud.asr_pause();
            }
        }

        /* Přerušení syntézy zasláním zprávy tts_stop */
        function do_tts_stop() {
            console.log("Sending tts_stop");
            speechCloud.tts_stop();
        }

        /* Syntéza řeči */
        function do_tts(text, voice) {
            speechCloud.tts_synthesize({
                text: text,
                voice: voice
            });
        }

        /* Obsluha tlačítka Restart dialog */
        $("#dialog-restart").click(function () {
            // TODO: nechci restart, chci jen start dialogu. je to mozne?
            location.reload(true);
        });

        /* Obsluha tlačítka pause dialog */
        // $("#dialog-pause").click(function () {
        //     if (dialogue_paused){
        //         const pauseIcon = document.getElementById('dialog-pause');
        //         pauseIcon.innerHTML = `
        //             <span class="material-symbols-outlined">
        //                 mic
        //             </span>`;
        //         dialogue_paused = false;
        //         speechCloud.dm_send_message({data: 'app'});
        //         console.log('spoustim dialog')
        //         const stateIcon = document.getElementById('state-icon');
        //         stateIcon.className = 'state-icon-recognizing';
        //         stateIcon.innerHTML = '';
        //         stateIcon.style.display = "block";
        //     }
        //     else {
        //         dialogue_paused = true;
        //         const pauseIcon = document.getElementById('dialog-pause');
        //         pauseIcon.innerHTML = `
        //             <span class="material-symbols-outlined">
        //                 mic_off
        //             </span>`;
        //         const stateIcon = document.getElementById('state-icon');
        //         stateIcon.className = 'state-icon-finished'; // Remove the loading class
        //         stateIcon.style.display = 'block'; // Ensure it's displayed
        //         stateIcon.innerHTML = `
        //             <span class="material-symbols-outlined">
        //                 pause
        //             </span>`;
        //         speechCloud.dm_send_message({data: 'app'});
        //         console.log('pauzuju dialog')
        //     };
        // });

        /* Obsluha tlačítka Stop dialog*/
        $("#dialog-stop").click(function () {
            hlog("<b>Terminating dialog</b>");
            speechCloud.terminate();
        });

        /* Obsluha tlačítka Recognition start/stop */
        $("#recog").click(function () {
            if (recognizing) {
                do_pause();
            } else {
                do_recognize();
            };
        });


        /* Po stisk mezerníku je totéž jako stisknutí tlačítka #recog */
        $(window).keydown(function(evt) {
            if (ignore_space) return;

            if (evt.keyCode == 32) {
                evt.preventDefault();
            };
        });

        $(window).keyup(function(evt) {
            if (ignore_space) return;

            if (evt.keyCode == 32) {
                setTimeout(function () {$("#recog").click()}, 100);
                evt.preventDefault();
            };
        });


        $("#file-input").change(function (e) {
            var file = e.target.files[0];
            if (!file) {
                return;
            }

            speechCloud.asr_offline_start();

            var reader = new FileReader();

            CHUNK_SIZE = 100*1024;
            start = 0;

            // Closure to capture the file information.
            reader.onloadend = function(evt) {
                if (evt.target.readyState == FileReader.DONE) {
                    var result = evt.target.result;
                    n_bytes = result.length;
                    hlog("<b>Sending "+n_bytes+" bytes from "+file.name+"</b>");
                    speechCloud.asr_offline_push_data({data: result});

                    load_next()
                }
            }

            function load_next() {
                if (start < file.size) {
                    var blob = file.slice(start, start+CHUNK_SIZE);
                    reader.readAsBinaryString(blob);
                    start += CHUNK_SIZE;
                } else {
                    speechCloud.asr_offline_stop();
                };
            };

            load_next()
        });


        /* Proměnná, do které se uloží timeout pro SIP zavolání */
        var call_timeout = null;

        /* Model URI je SPEECHCLOUD_URI a parametr z location.search */
        var model_uri = "https://prod.speechcloud.kky.zcu.cz:9443/v1/speechcloud/edu-brabenec"

        var options = {
            uri: model_uri,
            tts: "#audioout",
            disable_audio_processing: true
        }

        var speechCloud = new SpeechCloud(options);

        window.speechCloud = speechCloud

        // prichozi zprava z dm
        speechCloud.on('dm_receive_message', function (msg) {
            console.log('msg: ')
            console.log(msg)
            // if (msg.data.message == "app"){
            //     const stateIcon = document.getElementById('state-icon');
            //     stateIcon.className = 'state-icon-finished'; // Remove the loading class
            //     stateIcon.style.display = 'block'; // Ensure it's displayed
            //     stateIcon.innerHTML = `
            //         <span class="material-symbols-outlined">
            //             pause
            //         </span>`;
            //     dialogue_paused = true
            //     const pauseIcon = document.getElementById('dialog-pause');
            //     pauseIcon.innerHTML = `
            //         <span class="material-symbols-outlined">
            //             mic_off
            //         </span>`;
            // }
            if (msg.data.data.shopping_lists) {
                shop = msg.data.data.shopping_lists[0].items; 
                events = msg.data.data.events;  
                console.log("events received: ");
                console.log(events);
                console.log("shopping lists received: ");
                console.log(shop);

                populateEvents(events);
                populateShoppingList(shop);
            }
            else if (msg.data.data) {
                let dialogue_sentence = msg.data.data;
                console.log('asistent rekl: ');
                console.log(dialogue_sentence);
                addChatMessage(dialogue_sentence, true);
            }
            
        });

        speechCloud.on('error_init', function (data) {
            console.error('error.init event handler', data.status, data.text);
        });

        speechCloud.on('error_ws_initialized', function () {
            hlog('[WS] - ERROR: WS already initialized.');
        });

        speechCloud.on('_ws_connected', function () {
            hlog('[WS] - connected');
        });

        speechCloud.on('_ws_close', function () {
            hlog('[WS] - closed');
        });

        speechCloud.on('_ws_session', function (data) {
            hlog('[WS] - session started id=' + data.id);
        });

        speechCloud.on('_sip_closed', function (data) {
            hlog('[SIP] - closed');
            // if (!dialogue_paused){
                const stateIcon = document.getElementById('state-icon');
                stateIcon.className = 'state-icon-finished'; // Remove the loading class
                stateIcon.style.display = 'block'; // Ensure it's displayed
                stateIcon.innerHTML = `
                    <span class="material-symbols-outlined">
                        done_all
                    </span>`;
            // }
        });

        speechCloud.on('_sip_initializing', function (data) {
            hlog('[SIP] - client id=' + data);
            const stateIcon = document.getElementById('state-icon');
            stateIcon.className = 'state-icon-loading';
            stateIcon.innerHTML = '';
            stateIcon.style.display = "block";
        });

        speechCloud.on('_sip_registered', function () {
            hlog('[SIP] - registered');
        }); 

        speechCloud.on('asr_recognizing', function () {
            recognizing = true;
            hlog("<i><small>ASR start</small></i>")
            // if (!dialogue_paused){
                const stateIcon = document.getElementById('state-icon');
                stateIcon.className = 'state-icon-recognizing';
                stateIcon.innerHTML = '';
                stateIcon.style.display = "block";
            // }
        });

        speechCloud.on('asr_paused', function () {
                recognizing = false;
                hlog("<i><small>ASR stop</small></i>")
        });

        /* Při příchodu asr_ready (ASR připraveno) */
        speechCloud.on('asr_ready', function () {
            hlog("<b>ASR ready</b>");
            const stateIcon = document.getElementById('state-icon');
            stateIcon.className = 'state-icon-ready'; 
            stateIcon.style.display = 'block'; 
            stateIcon.innerHTML = `
                <span class="material-symbols-outlined">
                    person_check
                </span>`;
            // if (dialogue_paused){
            //     stateIcon.className = 'state-icon-ready'; 
            //     stateIcon.style.display = 'block'; 
            //     stateIcon.innerHTML = `
            //         <span class="material-symbols-outlined">
            //             pause
            //         </span>`;
            // }
        });

        /* Při příchodu požadavku na zobrazení z dialog manageru*/
        speechCloud.on('dm_display', function (msg) {
            hlog("<b>DISPLAY: "+msg.text+"</b>");
            console.log("dm_display", msg);

        });

        /* Při příchodu ASR výsledku */
        speechCloud.on('asr_result', function (msg) {
            if (msg.partial_result) {
                return;
            }
            hlog(msg.result);
            console.log("Result", msg);
            
            let result = msg.result;

            if ((result != '' && !message_already_sent_flag && result) /*&& !dialogue_paused*/){
                result = result.split('_').join(' ');
                console.log('Result', result);
                addChatMessage(result, false);
            }

            message_already_sent_flag = false
            /* zastavíme TTS */
            // do_tts_stop();

            // tts_result = msg.result.replace(/\[[^ ]+\]/g, ' ');

            // /* sesyntetizujeme odpověď */
            // engine = 'BDL';
            // ssml = "<?xml version='1.0' encoding='UTF-8'?>\n<speak version='1.0'> \n \n  <noise name='plane_jet3' type='continuous' subtype='plane' fVolume='1.00'/> \n  <noise name='radioswitch1' type='instant' subtype='switch' fVolume='0.5' /> \n  \n <noise name='signal_drop' type='random' subtype='drop' start='0' end='-1' iDropMinLen='100' iDropMaxLen='200' fVolMin='0.20' fVolMax='0.50' iWaitMin='2000' iWaitMax='7000'/> \n  <noise name='radioswitch1' type='instant' subtype='switch' fVolume='0.5'/> \n \n  <voice engine='"+engine+"'> \n    <prosody rate='+40%' pitch='-0%' fVolume='+40%'> \n      <s>"+tts_result+"</s> \n    </prosody> \n  </voice> \n</speak>";
            // do_tts(ssml);
        });

        /* Při skončení TTS */
        speechCloud.on('tts_done', function () {
            hlog("<i>TTS finished</i>");
        });

        /* Při příchodu sémantických entit ze SLU */
        speechCloud.on('slu_nbest', function (msg) {
            html = "<table><tr><th>n</th><th>prob</th><th>hyp</th></tr>";
            $(msg.nbest).each(function(index, hyp) {
                prob = hyp.prob.toFixed(3);
                html += "<tr><td>"+(index+1)+"</td><td>"+prob+"</td><td>"+hyp.hyp+"</td></tr>";
            });
            html += "</table>";
            hlog(html);
            console.log(msg.nbest);
        });

        /* Při příchodu sémantických entit ze SLU */
        speechCloud.on('slu_entities', function (msg) {
            html = "<table><tr><th>n</th><th>prob</th><th>entities</th></tr>";
            $(msg.entities).each(function(index, hyp) {
                prob = hyp.prob.toFixed(3);
                str = hyp.values.join(', ');
                html += "<tr><td>"+(index+1)+"</td><td>"+prob+"</td><td>"+str+"</td></tr>";
            });
            html += "</table>";
            hlog(html);
            console.log("slu_entities: ", msg);
            console

            console.log('slu_entities_len', msg.entities[0].values.length)
            if (msg.entities[0].values.length != 0 /*&& !dialogue_paused*/){
                const stateIcon = document.getElementById('state-icon');
                stateIcon.className = 'state-icon-tts'; // Remove the loading class
                stateIcon.style.display = 'block'; // Ensure it's displayed
                stateIcon.innerHTML = `
                    <span class="material-symbols-outlined">
                        person
                    </span>`;
            }
        })

        speechCloud.on('asr_audio_record', function (msg) {
            hlog("<b>ASR audio</b> <a href='"+ msg.uri +"' target='_blank'>" + msg.id + "</a>, tstamp="+msg.tstamp);
        });

        speechCloud.on('sc_start_session', function (msg) {
            hlog("<b>Session started</b> <a href='"+ msg.session_uri +"?format=yaml.html' target='_blank'>" + msg.session_id + "</a>");
            hlog("<b>JSON schema URI</b> <a href='"+ msg.schema_uri +"?format=docson' target='_blank'>" + msg.schema_uri + "</a>");
            hlog("<b>SpeechCloud model URI</b> <a href='"+ model_uri +"' target='_blank'>" + model_uri + "</a>");

            console.log(msg.schema);

            hlog('[LIB] - Methods: ' + this.availableMethods().join(', '));
            hlog('[LIB] - Events: ' + this.availableEvents().join(', '));
        });

        speechCloud.on('sc_error', function (msg) {
            hlog("<b>Error</b> in method <b>"+msg.method_name+"</b> <br>" + msg.error);
            console.log(msg);
        });

        speechCloud.on('itblp_gen_grammar_result', function (msg) {
            hlog("<b>Generated grammar of type </b> " + msg.se_type + "<pre>"+msg.grammar+"</pre>");

            speechCloud.slu_set_grammars(
                {"grammars": [
                    {"entity":"ALT", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/ALT.abnf"},
                    {"entity":"CMD", "type":"abnf", "data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/CMD.abnf"},
                    {"entity":"CS","type":"abnf-inline","data":msg.grammar},
                    {"entity":"FL","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FL.abnf"},
                    {"entity":"FR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/FR.abnf"},
                    {"entity":"HE","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/HE.abnf"},
                    {"entity":"PO","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/PO.abnf"},
                    {"entity":"QNH","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/QNH.abnf"},
                    {"entity":"RA","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/RA.abnf"},
                    {"entity":"SP","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SP.abnf"},
                    {"entity":"SQ","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/SQ.abnf"},
                    {"entity":"TU","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TU.abnf"},
                    {"entity":"TWR","type":"abnf","data":"http://itblp.zcu.cz/app-demo/atg1/static/grms/TWR.abnf"}
                ]});
        });

        speechCloud.on("asr_offline_started", function (msg) {
            hlog("<i><small>ASR start / offline</small></i>")
        });

        speechCloud.on("asr_offline_finished", function (msg) {
            hlog("<i><small>ASR stop / offline</small></i>")
        });

        speechCloud.on("asr_offline_error", function (msg) {
            hlog("<i><small>ASR error / offline</small></i>")
        });



        speechCloud.init();

});
