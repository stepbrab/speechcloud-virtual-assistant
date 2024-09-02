from dialog import SpeechCloudWS, Dialog
import logging
import datetime
import grammars
import json
from frame import CalendarEventFrame, ShoppingListFrame, ShoppingItemFrame


TIMEOUT = 100.

class DialogueManager(Dialog):
    task = None
    # dialogue_started = False
    
    def ask_for_missing_event_frame_entities(self, frame):
        """
        Asks the user for missing entities of a frame

        Args:
            frame: calendar event frame

        Returns:
            list of missing frame entities to ask the user for
        """
        
        missing_entities = []
        if frame.date_day == None:
            missing_entities.append('den')
            
        if frame.date_month == None:
            missing_entities.append('měsíc')
            
        # if frame.date_year == None:
        #     missing_entities.append('rok')
            
        if frame.time_start == None:
            missing_entities.append('čas začátku')
        
        if frame.time_end == None:
            missing_entities.append('čas konce')
        
        return missing_entities
        
    def fill_event_frame(self, result, frame):
        """
        Based on the result of slu, fills the calendar event frame

        Args:
            result: result of speech recognition
            frame: calendar event frame

        Returns:
            filled event frame
        """
        
        if result.entities['event'] and frame.event_type == None:
            frame.event_type = result.entities['event'].first   
            
        if result.entities['relative_day'] and frame.date_day == None and frame.date_month == None and frame.date_year == None:
            if 'dnes' in result.entities['relative_day']:
                date = datetime.date.today()
                frame.date_day = f"{date.day}."
                frame.date_month = f"{date.month}."
                frame.date_year = str(date.year)
                
            elif 'zitra' in result.entities['relative_day']:
                date = datetime.date.today() + datetime.timedelta(days = 1)
                frame.date_day = f"{date.day}."
                frame.date_month = f"{date.month}."
                frame.date_year = str(date.year)
                
            elif 'pozitra' in result.entities['relative_day']:
                date = datetime.date.today() + datetime.timedelta(days = 2)
                frame.date_day = f"{date.day}."
                frame.date_month = f"{date.month}."
                frame.date_year = str(date.year)
                print(frame)
                
        if result.entities['weekday'] and frame.date_day == None and frame.date_month == None and frame.date_year == None:
            weekday = int(result.entities['weekday'].first)
            today = datetime.date.today()
                            
            if result.entities['relative_week']:
                if 'tento' in result.entities['relative_week']:
                    days_offset = weekday - today.weekday()
                    
                elif 'pristi' in result.entities['relative_week']:
                    days_offset = weekday - today.weekday()
                    days_offset += 7
            
            else:
                days_offset = weekday - today.weekday()
                if days_offset < 0:
                    days_offset += 7  
            
            if days_offset < 0:
                date = today - datetime.timedelta(days = -days_offset)
            else:
                date = today + datetime.timedelta(days = days_offset)
                
            frame.date_day = f"{date.day}."
            frame.date_month = f"{date.month}."
            frame.date_year = str(date.year)
            
                    
        if result.entities['date_d'] and frame.date_day == None:               
            frame.date_day = result.entities['date_d'].first
            
        if result.entities['date_m'] and frame.date_month == None:    
            frame.date_month = result.entities['date_m'].first
            
        if result.entities['date_y'] and frame.date_year == None:  
            frame.date_year = result.entities['date_y'].first
                    
        if result.entities['length'] and frame.time_start == None and frame.time_end == None:
            if '24' in result.entities['length']:
                frame.time_start = '00:00'
                frame.time_end = '23:59'
                    
        if result.entities['time']:
            if len(result.entities['time']) > 1 and (frame.time_end == None or frame.time_start == None):
                times = result.entities['time'].all
                frame.time_start = times[0]
                frame.time_end = times[1]   
            
            elif frame.time_start == None:
                frame.time_start = result.entities['time'].first
                
            elif frame.time_end == None:
                frame.time_end = result.entities['time'].first
                
        if result.entities['length'] and frame.time_end == None:
            frame.time_end = self.length_input_handler(frame.time_start, result.entities['length'].first)
        
        if frame.date_year == None and frame.date_day != None:
            today = datetime.date.today()
            frame.date_year = str(today.year) 
        
        if frame.time_start != None and frame.time_end != None:
            hours, minutes = map(int, frame.time_start.split(':'))
            start_time = datetime.datetime(year=1, month=1, day=1, hour=hours, minute=minutes) 
            hours, minutes = map(int, frame.time_end.split(':'))
            end_time = datetime.datetime(year=1, month=1, day=1, hour=hours, minute=minutes)
        
            if start_time > end_time:
                temp = frame.time_end
                frame.time_end = frame.time_start
                frame.time_start = temp
                
            min_time = datetime.time(6, 0) 
            max_time = datetime.time(20, 0)  
                
            if start_time.time() < min_time:
                frame.time_start = '6:00'
                
            if end_time.time() > max_time:
                frame.time_end = '20:00'
             
        if frame.complete == False and frame.event_type != None and frame.date_day != None and frame.date_month != None and frame.date_year != None and frame.time_start != None and frame.time_end != None:
            frame.complete = True
            
            event = {
                'type': frame.event_type,
                'date_day': frame.date_day,
                'date_month': frame.date_month,
                'date_year': frame.date_year,
                'time_start': frame.time_start, 
                'time_end': frame.time_end
            }
                    
            return event

    def length_input_handler(self, time_start, length):
        """
        Calculates the end time based on the given start time and length (in hours and minutes).

        Args:
            time_start: The start time
            length: The length of the event in hours

        Returns:
            The calculated end time
        """

        # Convert time_start to datetime object
        if time_start != None:
            hours, minutes = map(int, time_start.split(':'))
            start_time = datetime.datetime(year=1, month=1, day=1, hour=hours, minute=minutes)

            # Convert length string to float
            length_hours = float(length)

            # Convert length to timedelta
            length_timedelta = datetime.timedelta(hours=length_hours)

            # Add length to start time
            end_time = start_time + length_timedelta

            # Format end time back to 'HH:MM'
            return end_time.strftime('%H:%M')
    
    


    async def main(self):
        with open("./data.json", "r") as file1:
            data = json.load(file1)    

            await self.send_message({"message": "last_id", "data": data})
            self.logger.debug(f"poslal jsem data")
            
        self.logger.debug(f"halo jsem tady")
        frame = None
        # self.task = 'aplikace'
        alive_check = 0
        
        another_command_check = False
        
        # Load grammars
        grammar = self.grammar_from_dict('relative_week', grammars.RELATIVNI_TYDEN)
        grammar += self.grammar_from_dict('relative_day', grammars.RELATIVNI_DEN)
        grammar += self.grammar_from_dict('weekday', grammars.DEN_TYDNU)
        grammar += self.grammar_from_dict('date_d', grammars.DATUM_DEN)
        grammar += self.grammar_from_dict('date_m', grammars.DATUM_MESIC)
        grammar += self.grammar_from_dict('date_y', grammars.DATUM_ROK)
        grammar += self.grammar_from_dict('time', grammars.CAS)
        grammar += self.grammar_from_dict('length', grammars.DELKA)
        grammar += self.grammar_from_dict('item', grammars.POLOZKA)
        grammar += self.grammar_from_dict('count', grammars.POCET)
        grammar += self.grammar_from_dict('event', grammars.AKCE)
        grammar += self.grammar_from_dict('shop', grammars.NAKUP)
        grammar += self.grammar_from_dict('command', grammars.COMMANDS)
        await self.define_slu_grammars(grammar)

        announcement = "Zdravím, co si přejete? Pro nápovědu použijte příkaz nápověda."
        await self.send_message({"message": "last_id", "data": announcement})
        await self.synthesize_and_wait(announcement)
        
        
        
        while True:
            
            # break if frame is complete and no more commands are given
            if frame != None:
                if frame.complete:
                    announcement = 'Přejete si ještě něco?'
                    another_command_check += 1
                    await self.send_message({"message": "last_id", "data": announcement})
                    result = await self.synthesize_and_wait_for_slu_result(announcement, timeout=TIMEOUT)
                    if result.entities['command']:
                        if 'ne' in result.entities['command']:
                            announcement = 'Dobře, končím.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            frame = None
                            self.task = None
                            break
                        elif 'ano' in result.entities['command']:
                            announcement = 'Dobře, co si přejete?'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            frame = None
                            self.task = None
                            another_command_check = False
                            continue
                        else:
                            another_command_check = True
                            frame = None
                            self.task = None
                            continue
                    else:
                        announcement = 'Končím tedy.'
                        await self.send_message({"message": "last_id", "data": announcement})
                        await self.synthesize_and_wait(announcement)
                        break
            
            # user input
            if another_command_check == False:
                result = await self.recognize_and_wait_for_slu_result(timeout=TIMEOUT)      
            else:
                another_command_check = False  
            # if self.task != 'aplikace':
            
            if not result.entities['command'] and self.task == None:
                print('alive check')
                alive_check += 1
                if alive_check == 1:
                    announcement = 'Prosím zadejte příkaz.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    continue
                elif alive_check == 2:
                    announcement = 'Prosím zadejte příkaz, nebo dialog ukončím.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    continue
                else:
                    announcement = 'Ukončuji dialog, nebyl zadán příkaz.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    break
                
            command = result.entities['command']

            # TODO: lepsi by bylo mit zvlast ramec na vubec urceni self.tasku..    
            if frame == None and self.task == None:
                print('self.task')
                if 'ahoj' in command:
                    announcement = 'Zdravím. Přejete si?'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    continue
                    
                elif 'pomoc' in command:
                    self.task = 'pomoc'
                    frame = CalendarEventFrame() #dummy frame
                    frame.complete = True #dummy frame
                    
                # elif 'aplikace' in command:
                #     frame = CalendarEventFrame() #dummy frame
                #     self.task = 'aplikace'
                #     announcement = 'Dobře, pozastavuji dialog. Pro použití hlasového ovládání restartujte dialog stisknutím tlačítka "play" v levém horním rohu aplikace.'
                #     await self.send_message({"message": "last_id", "data": announcement})
                #     await self.synthesize_and_wait(announcement)
                #     await self.send_message({"message": "app"})
                    
                elif 'vytvor' in command:
                    if result.entities['event'] or 'akce' in command:
                        self.task = 'vytvor_akci'
                        frame = CalendarEventFrame()
                    elif result.entities['shop'] or result.entities['item']:
                        self.task = 'pridej_polozku'
                        frame = ShoppingListFrame()
                        
                elif 'rekni' in command:
                    if result.entities['event'] or 'akce' in command:
                        self.task = 'rekni_akci'
                        frame = CalendarEventFrame()
                    elif result.entities['shop'] or result.entities['item']:
                        self.task = 'rekni_nakup'
                        frame = ShoppingListFrame()
                        
                elif 'smaz' in command:
                    if result.entities['event'] or 'akce' in command:
                        self.task = 'smaz_akci'
                        frame = CalendarEventFrame()
                    elif result.entities['shop'] or result.entities['item']:
                        self.task = 'smaz_polozku'
                        frame = ShoppingListFrame()
                      
                    
                if self.task == None:
                    announcement = 'Nerozumím. Prosím zopakujte váš požadavek.'
                    await self.send_message({"message": "last_id", "data": announcement})    
                    await self.synthesize_and_wait(announcement)
                    continue
             
            print('Řeším úkol ' + self.task)
            
            if self.task == 'pomoc':
                announcement = 'Pro změnu barevného téma aplikace použijte klávesovou zkratku ALT plus Té. Pro správu kalendářních akcí použijte příkazy jako "vytvoř událost", "odeber událost", či "co mám naplánováno". Pro správu nákupního seznamu použijte příkazy typu "přidej položku", "odeber položku" a nebo "co mám v nákupním seznamu".' # Pokud chcete pouze používat aplikaci bez dialogu, použijte příkaz "zůstat v aplikaci".
                await self.send_message({"message": "last_id", "data": announcement})
                await self.synthesize_and_wait(announcement)
                continue
            
            elif self.task == 'vytvor_akci':
                event = self.fill_event_frame(result, frame)
                
                if frame.complete == True:
                    print(event)
                    announcement = 'Opravdu chcete vytvořit událost typu ' + event['type'] + ' na den ' + event['date_day'] + event['date_month'] + event['date_year'] + ', od ' + event['time_start'] + ' do ' + event['time_end'] + '?'
                    await self.send_message({"message": "last_id", "data": announcement})
                    result = await self.synthesize_and_wait_for_slu_result(announcement, timeout=TIMEOUT)
                    if result.entities['command']:
                        if 'ne' in result.entities['command']:
                            announcement = 'Omlouvám se, prosím zadejte požadavek znovu.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            result = await self.synthesize_and_wait(announcement)
                            frame = None
                            self.task = None
                            continue
                        elif 'ano' in result.entities['command']:
                            announcement = 'Dobře, vytvářím událost.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            result = await self.synthesize_and_wait(announcement)
                            with open("data.json", "r+") as json_file:
                                data = json.load(json_file) 

                                data["events"].append(event)
                                
                                json_file.seek(0)

                                json.dump(data, json_file, indent=4) 
                                json_file.truncate()
                                json_file.seek(0)
                                
                                await self.send_message({"message": "last_id", "data": data})
                                self.logger.debug(f"poslal jsem data")
                                
                            self.task = None
                            
                        else:
                            continue
                    else:
                        print('error')
                    continue
                    
                else:
                    missing_entities = self.ask_for_missing_event_frame_entities(frame)
                    if len(missing_entities) == 1:
                        missing_entity_string = str(missing_entities[0])
                    else:
                        missing_entity_string = ", ".join(f"{entity}" for entity in missing_entities[:-1]) + " a " + missing_entities.pop()
                    print(missing_entity_string)
                    announcement = 'Prosím specifikujte ' + missing_entity_string + ' události.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    result = await self.synthesize_and_wait(announcement)
                    continue
                
            elif self.task == 'smaz_akci':
                event_by_type = False
                if 'vsechny' in result.entities['command']:
                    frame.time_start = '00:00'
                    frame.time_end = '23:59'
                
                elif result.entities['event'] and not result.entities['time']: # TODO: zakomponovat do fill event frame
                    frame.time_start = '00:00'
                    frame.time_end = '23:59'
                    event_by_type = True
                        
                event = self.fill_event_frame(result, frame)
                
                if frame.complete == True:
                    print(event)
                
                    events_to_keep = []  
                    
                    with open('data.json', "r+") as json_file:
                        data = json.load(json_file)
                        events_to_keep = []

                        event_start = datetime.datetime.strptime(event.get('time_start'), '%H:%M').time()
                        event_end = datetime.datetime.strptime(event.get('time_end'), '%H:%M').time()

                        announcement = "Přejete si opravdu smazat tyto události "
                        found_event = False
                        for saved_event in data["events"]:
                            saved_event_start = datetime.datetime.strptime(saved_event.get('time_start'), '%H:%M').time()
                            saved_event_end = datetime.datetime.strptime(saved_event.get('time_end'), '%H:%M').time()

                            if not event_by_type and (saved_event.get('date_year') == event.get('date_year') and
                                saved_event.get('date_month') == event.get('date_month') and
                                saved_event.get('date_day') == event.get('date_day') and
                                (((event_start <= saved_event_start <= event_end) and
                                (event_start <= saved_event_end <= event_end)))):
                                print(saved_event)
                                announcement += str(saved_event['type']) + ' ' + str(saved_event['date_day']) + str(saved_event['date_month']) + str(saved_event['date_year']) + ', od ' + str(saved_event['time_start']) + ' do ' + str(saved_event['time_end']) + ', '
                                found_event = True
                                continue
                            
                            elif event_by_type and (saved_event.get('date_year') == event.get('date_year') and
                                saved_event.get('date_month') == event.get('date_month') and
                                saved_event.get('date_day') == event.get('date_day') and
                                saved_event.get('type') == frame.event_type):
                                print(saved_event)
                                announcement += str(saved_event['type']) + ' ' + str(saved_event['date_day']) + str(saved_event['date_month']) + str(saved_event['date_year']) + ', od ' + str(saved_event['time_start']) + ' do ' + str(saved_event['time_end']) + ', '
                                found_event = True
                                continue
                                
                            
                            else:
                                events_to_keep.append(saved_event)

                        announcement = announcement[:-2] + "?"
                        data["events"] = events_to_keep
                        if not found_event:
                            announcement = 'Taková událost neexistuje.'
                            self.task = None
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            continue
                        
                        await self.send_message({"message": "last_id", "data": announcement})
                        result = await self.synthesize_and_wait_for_slu_result(announcement, timeout=TIMEOUT)
                        
                        if result.entities['command']:
                            if 'ne' in result.entities['command']:
                                announcement = 'Omlouvám se, prosím zadejte požadavek znovu.'
                                await self.send_message({"message": "last_id", "data": announcement})
                                await self.synthesize_and_wait(announcement)
                                frame = None
                                self.task = None
                                continue
                            
                            elif 'ano' in result.entities['command']:
                                announcement = 'Dobře, mažu události.'
                                await self.send_message({"message": "last_id", "data": announcement})
                                await self.synthesize_and_wait(announcement)
                                
                                json_file.seek(0)
                                json.dump(data, json_file, indent=4)
                                json_file.truncate()
                                self.task = None
                                
                                await self.send_message({"message": "last_id", "data": data})
                                self.logger.debug(f"poslal jsem data")
                                
                            else:
                                continue
                
                else:
                    missing_entities = self.ask_for_missing_event_frame_entities(frame)
                    if len(missing_entities) == 1:
                        missing_entity_string = str(missing_entities[0])
                    else:
                        missing_entity_string = ", ".join(f"{entity}" for entity in missing_entities[:-1]) + " a " + missing_entities.pop()
                    print(missing_entity_string)
                    announcement = 'Prosím specifikujte ' + missing_entity_string + '.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    continue
            
            elif self.task == 'rekni_akci':
                found_event = False
                
                frame.event_type = 'dummy_type'
                        
                event = self.fill_event_frame(result, frame)
                
                if (frame.time_start == None) and (frame.time_end == None):
                    frame.time_start = '00:00'
                    frame.time_end = '23:59'
                    event = self.fill_event_frame(result, frame)
                
                if frame.complete == True:
                    print(event)
                
                    events_to_keep = []  
                    
                    with open("data.json", "r") as infile:
                        data = json.load(infile)
                                
                    
                    if frame.time_start != '6:00' and frame.time_end != '20:00':
                        announcement = 'V časovém intervalu od ' + event['time_start'] + ' do ' + event['time_end'] + ' máte naplánováno '
                    else:
                        announcement = 'Na den ' + event['date_day'] + event['date_month'] + event['date_year'] + ' máte naplánováno '
                    
                    event_start = datetime.datetime.strptime(event.get('time_start'), '%H:%M').time()
                    event_end = datetime.datetime.strptime(event.get('time_end'), '%H:%M').time()
                       
                    for saved_event in data["events"]:
                        saved_event_start = datetime.datetime.strptime(saved_event.get('time_start'), '%H:%M').time()
                        saved_event_end = datetime.datetime.strptime(saved_event.get('time_end'), '%H:%M').time()

                        if (saved_event.get('date_year') == event.get('date_year') and
                            saved_event.get('date_month') == event.get('date_month') and
                            saved_event.get('date_day') == event.get('date_day') and
                            (event_start <= saved_event_start <= event_end) and
                            (event_start <= saved_event_end <= event_end)):
                            found_event = True
                            announcement += saved_event['type'] + ' od ' + saved_event['time_start'] + ' do ' + saved_event['time_end'] + ', '
                    
                    announcement = announcement[:-2] + "."
                    if not found_event:
                        if frame.time_start != '6:00' and frame.time_end != '20:00':
                            announcement = 'V časovém intervalu od ' + event['time_start'] + ' do ' + event['time_end'] + ' máte volno.'
                        else:
                            announcement = 'V den ' + event['date_day'] + event['date_month'] + event['date_year'] + ' máte volno.'
                        
                    await self.send_message({"message": "last_id", "data": announcement}) 
                    await self.synthesize_and_wait(announcement)   
                    continue
                        
                else:
                    missing_entities = self.ask_for_missing_event_frame_entities(frame)
                    print(len(missing_entities))
                    if len(missing_entities) == 1:
                        missing_entity_string = str(missing_entities[0])
                    else:
                        missing_entity_string = ", ".join(f"{entity}" for entity in missing_entities[:-1]) + " a " + missing_entities.pop()
                    print(missing_entity_string)
                    announcement = 'Prosím specifikujte ' + missing_entity_string + ' události.'
                await self.send_message({"message": "last_id", "data": announcement})
                await self.synthesize_and_wait(announcement)
                continue
             
            # TODO: vyresit handling poctu polozek, jak vedet ktery pocet patri ke ktere polozce z vysledku slu - 
                # jak sahnout na hodnotu begin a end v entity? tim by to vlastne slo poresit, checknul bych begin te dane polozky a zda ma pred sebou info o poctu
                # workaround: nutnost specifikace poctu polozek pro kazdou polozku nakupu 
            elif self.task == 'pridej_polozku':
                if (not result.entities['count']) or (len(result.entities['item']) != len(result.entities['count'])):
                    announcement = 'Prosím specifikujte počet každé položky.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    continue
                
                if result.entities['item'] and result.entities['count']:
                    counts = result.entities['count'].all
                    items = result.entities['item'].all
                    
                    announcement = "Přejete si opravdu přidat položky "
                    
                    frame.complete = True # TODO: frame je zbytecnej vlastne.. 
                    
                    for i in range(len(items)):
                        specific_item = ShoppingItemFrame()
                        specific_item.name = items[i]
                        specific_item.amount = int(counts[i])
                        specific_item.complete = True # TODO: vzdy complete, problem s tema poctama
                        frame.items.append(specific_item)
                        announcement += str(specific_item.amount) + 'krát ' + str(items[i]) + ', '   
                    
                    announcement = announcement[:-2] + "?"    
                    await self.send_message({"message": "last_id", "data": announcement})
                    result = await self.synthesize_and_wait_for_slu_result(announcement, timeout=TIMEOUT)
                        
                    if result.entities['command']:
                        if 'ne' in result.entities['command']:
                            announcement = 'Omlouvám se, prosím zadejte požadavek znovu.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            frame = None
                            self.task = None
                            continue
                        
                        elif 'ano' in result.entities['command']:
                            announcement = 'Dobře, přidávám položky.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            
                            with open('data.json', "r+") as json_file:
                                data = json.load(json_file)
                                
                                found = False 

                                for item in frame.items:
                                    for existing_item in data['shopping_lists'][0]['items']:
                                        if existing_item['name'] == item.name:
                                            existing_item['amount'] += item.amount
                                            found = True
                                            break  

                                    if not found:
                                        data['shopping_lists'][0]['items'].append({'name': item.name, 'amount': item.amount})
                                        found = False 
                                        
                                json_file.seek(0)
                                json.dump(data, json_file, indent=4)
                                json_file.truncate()
                                json_file.seek(0)
                                
                                data = json.load(json_file)
                                await self.send_message({"message": "last_id", "data": data})
                                self.logger.debug(f"poslal jsem data")
                                self.task = None
                                
                        else:
                            continue
                
                else:
                    announcement = 'Prosím specifikujte položky a jejich počet, jež chcete přidat do nákupního seznamu.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    continue     
                
            elif self.task == 'smaz_polozku':
                if 'vsechny' in command:
                    with open('data.json', "r+") as json_file:
                        data = json.load(json_file)
                        
                        if len(data['shopping_lists'][0]['items']) == 0:
                            announcement = "Nákupní seznam již máte prázdný."
                            self.task = None
                            frame.complete = True
                            continue
                            
                    announcement = "Přejete si opravdu smazat všechny položky z nákupního seznamu?"
                    await self.send_message({"message": "last_id", "data": announcement})
                    result = await self.synthesize_and_wait_for_slu_result(announcement, timeout=TIMEOUT)
                    
                    if result.entities['command']:
                        if 'ne' in result.entities['command']:
                            announcement = 'Omlouvám se, prosím zadejte požadavek znovu.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            frame = None
                            self.task = None
                            continue
                        
                        elif 'ano' in result.entities['command']:
                            announcement = 'Dobře, mažu všechny položky.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            
                            with open('data.json', "r+") as json_file:
                                data = json.load(json_file)
                                
                                data['shopping_lists'][0]['items'] = []
                                
                                json_file.seek(0)
                                json.dump(data, json_file, indent=4)
                                json_file.truncate()
                                json_file.seek(0)
                                
                                data = json.load(json_file)
                                await self.send_message({"message": "last_id", "data": data})
                                self.logger.debug(f"poslal jsem data")
                                self.task = None
                                
                            frame.complete = True
                            continue
                        
                        else:
                            continue
                        
                elif result.entities['item']:
                    items = result.entities['item'].all
                    
                    if len(items) == 1:
                        announcement = "Přejete si opravdu smazat položku "
                    else:    
                        announcement = "Přejete si opravdu smazat položky "
                    
                    frame.complete = True # TODO: jen jeden nakupni seznam... frame je zbytecnej vlastne
                    
                    for i in range(len(items)):
                        specific_item = ShoppingItemFrame()
                        specific_item.name = items[i]
                        # specific_item.amount = 1 # TODO: tady bych to zatim nechal tak, ze neni moznost mazat jen napriklad 3 mleka, kdyz jich mam 6, je vzdy mozne jen smazat vsechny
                        specific_item.complete = True # TODO: vzdy complete, problem s tema poctama
                        frame.items.append(specific_item)
                        announcement += str(items[i]) + ', '  
                         
                    announcement = announcement[:-2] + "?"  
                    items_to_keep = [] 
                    with open('data.json', "r+") as json_file:
                        data = json.load(json_file)
                        found_item = False
                        for saved_item in data['shopping_lists'][0]['items']:
                            for item in frame.items:
                                if (saved_item['name'] == item.name):
                                    found_item = True
                                    continue
                                
                                else:
                                    items_to_keep.append(saved_item)
                            
                    
                    if not found_item:
                        announcement = 'Takovou položku v nákupním seznamu nemáte.'
                        self.task = None
                        await self.send_message({"message": "last_id", "data": announcement})
                        await self.synthesize_and_wait(announcement)
                        continue
                         
                    await self.send_message({"message": "last_id", "data": announcement})
                    result = await self.synthesize_and_wait_for_slu_result(announcement, timeout=TIMEOUT)
                        
                    if result.entities['command']:
                        if 'ne' in result.entities['command']:
                            announcement = 'Omlouvám se, prosím zadejte požadavek znovu.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            frame = None
                            self.task = None
                            continue
                        
                        elif 'ano' in result.entities['command']:
                            announcement = 'Dobře, mažu položky.'
                            await self.send_message({"message": "last_id", "data": announcement})
                            await self.synthesize_and_wait(announcement)
                            
                            with open('data.json', "r+") as json_file:
                                data = json.load(json_file)
                                
                                items_to_keep = []
                                
                                for saved_item in data['shopping_lists'][0]['items']:
                                    for item in frame.items:
                                        if (saved_item['name'] == item.name):
                                            continue
                                        
                                        else:
                                            items_to_keep.append(saved_item)
                                    
                                data['shopping_lists'][0]['items'] = items_to_keep
                            
                                json_file.seek(0)
                                json.dump(data, json_file, indent=4)
                                json_file.truncate()
                                json_file.seek(0)
                                
                                data = json.load(json_file)
                                await self.send_message({"message": "last_id", "data": data})
                                self.logger.debug(f"poslal jsem data")
                                self.task = None
                                
                        else:
                            continue
                
                else:
                    announcement = 'Prosím specifikujte položky, které chcete odstranit z nákupního seznamu.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    continue   
                
            elif self.task == 'rekni_nakup':
                with open('data.json', "r+") as json_file:
                    data = json.load(json_file)
                    
                    items_to_keep = []
                    
                    announcement = 'V nákupním seznamu máte položky '
                    
                    pos = -1
                    for saved_item in data['shopping_lists'][0]['items']:
                        pos += 1
                        announcement += str(saved_item['amount']) + 'krát ' + saved_item['name']
                        if pos == len(data['shopping_lists'][0]['items']) - 1:
                            announcement += '.'
                        else:
                            announcement += ', '
                    
                    if pos == -1:
                        announcement = 'Nákupní seznam je prázdný.'
                    await self.send_message({"message": "last_id", "data": announcement})
                    await self.synthesize_and_wait(announcement)
                    frame.complete = True

    def on_receive_message(self, data):
        print('prisla data')
        # if data == 'app':
        #     if self.task == 'aplikace':
        #         print('Spoustim dialog')
        #         self.task = None
        #     else:
        #         print('Pauzuju dialog')
        #         self.task = 'aplikace'
        # else:
        received_data = json.loads(data) 
        print(received_data)

        with open("data.json", "r+") as json_file:          
            json_file.seek(0)
        
            json.dump(received_data, json_file, indent=4)  
            
            json_file.truncate()

        self.logger.debug(f"dostal jsem data")
             
        
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s',level=logging.DEBUG)

    SpeechCloudWS.run(DialogueManager, address="0.0.0.0", port=8888, static_path="./static")

