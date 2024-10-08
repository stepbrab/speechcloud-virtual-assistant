#ABNF 1.0 UTF-8;

RELATIVNI_TYDEN = {
    'tento': {'tento', 'tenhle', 'tuten', 'tohle', 'tuhle', 'tuto', 'této', 'téhle', 'tato'},
    'pristi': {'příští', 'další', 'následující'},
}

DEN_TYDNU = {
    '0': {'pondělí', 'pondělek', 'pondělní'},
    '1': {'úterý', 'úterek', 'úterní'},
    '2': {'středa', 'středu', 'středeční', 'středy'},
    '3': {'čtvrtek', 'čtvrteční', 'čtvrtka'},
    '4': {'pátek', 'páteční', 'pátku', 'pátka'},
    '5': {'sobota', 'sobotu', 'sobotní', 'soboty'},
    '6': {'neděle', 'neděli', 'nedělní'}
}

RELATIVNI_DEN = {
    'dnes': {'dnes', 'dneska', 'dnešek', 'dnešní', 'dneška'},
    'zitra': {'zítra', 'zítřek', 'zítřejší', 'zítřka'},
    # 'pozitra': {'po_zítří', 'po_zítřek', 'po_zítřejší'}
}

DATUM_DEN = {
    '1.': {'prvního', '1.', '1'},
    '2.': {'druhého', 'druhýho', '2.', '2'},
    '3.': {'třetího', '3.', '3'},
    '4.': {'čtvrtého', 'čtvrtýho', '4.', '4'},
    '5.': {'pátého', 'pátýho', '5.', '5'},
    '6.': {'šestého', 'šestýho', '6.', '6'},
    '7.': {'sedmého', 'sedmýho', '7.', '7'},
    '8.': {'osmého', 'osmýho', '8.', '8'},
    '9.': {'devátého', 'devátýho', '9.', '9'},
    '10.': {'desátého', 'desátýho', '10.', '10'},
    '11.': {'jedenáctého', 'jedenáctýho', '11.', '11'},
    '12.': {'dvanáctého', 'dvanáctýho', '12.', '12'},
    '13.': {'třináctého', 'třináctýho', '13.', '13'},
    '14.': {'čtrnáctého', 'čtrnáctýho', '14.', '14'},
    '15.': {'patnáctého', 'patnáctýho', '15.', '15'},
    '16.': {'šestnáctého', 'šestnáctýho', '16.', '16'},
    '17.': {'sedmnáctého', 'sedmnáctýho', '17.', '17'},
    '18.': {'osmnáctého', 'osmnáctýho', '18.', '18'},
    '19.': {'devatenáctého', 'devatenáctýho', '19.', '19'},
    '20.': {'dvacátého', 'dvacátýho', '20.', '20'},
    '21.': {'dvacátého_prvního', 'dvacátýho_prvního', '21.', '21'},
    '22.': {'dvacátého_druhého', 'dvacátýho_druhýho', '22.', '22'},
    '23.': {'dvacátého_třetího', '23.', '23'},
    '24.': {'dvacátého_čtvrtého', 'dvacátýho_čtvrtýho', '24.', '24'},
    '25.': {'dvacátého_pátého', 'dvacátýho_pátýho', '25.', '25'},
    '26.': {'dvacátého_šestého', 'dvacátýho_šestýho', '26.', '26'},
    '27.': {'dvacátého_sedmého', 'dvacátýho_sedmýho', '27.', '27'},
    '28.': {'dvacátého_osmého', 'dvacátýho_osmýho', '28.', '28'},
    '29.': {'dvacátého_devátého', 'dvacátýho_devátýho', '29.', '29'},
    '30.': {'třicátého', 'třicátýho', '30.', '30'},
    '31.': {'třicátého_prvního', 'třicátýho_prvního', '31.', '31'}
}

DATUM_MESIC = {
    '1.' : {'leden', 'ledna', 'první', '1.', '1'},
    '2.' : {'únor', 'února', 'druhý', '2.', '2'},
    '3.' : {'březen', 'března', 'třetí', '3.', '3'},
    '4.' : {'duben', 'dubna', 'čtvrtý', '4.', '4'},
    '5.' : {'květen', 'května', 'pátý', '5.', '5'},
    '6.' : {'červen', 'června', 'šestý', '6.', '6'},
    '7.' : {'červenec', 'července', 'sedmý', '7.', '7'},
    '8.' : {'srpen', 'srpna', 'osmý', '8.', '8'},
    '9.' : {'září', 'devátý', '9.', '9'},
    '10.' : {'říjen', 'října', 'desátý', '10.', '10'},
    '11.' : {'listopad', 'listopadu', 'jedenáctý', '11.', '11'},
    '12.' : {'prosinec', 'prosince', 'dvanáctý', '12.', '12'}
}

DATUM_ROK = {
    '2023' : {'dva_tisíce_dvacet_tři', '2023'},
    '2024' : {'dva_tisíce_dvacet_čtyři', '2024'},
    '2025' : {'dva_tisíce_dvacet_pět', '2025'},
    '2026' : {'dva_tisíce_dvacet_šest', '2026'},
    '2027' : {'dva_tisíce_dvacet_sedm', '2027'},
    '2028' : {'dva_tisíce_dvacet_osm', '2028'},
    '2029' : {'dva_tisíce_dvacet_devět', '2029'},
    '2030' : {'dva_tisíce_třicet_deset', '2030'},
    '2031' : {'dva_tisíce_třicet_jedna', '2031'},
    '2032' : {'dva_tisíce_třicet_dva', '2032'},
    '2033' : {'dva_tisíce_třicet_tři', '2033'},
    '2034' : {'dva_tisíce_třicet_čtyři', '2034'}
}

CAS = {
    '6:00' : {'6', '6:00', 'šestou', 'šest','šest_nula_nula', 'šest_ráno', 'šest_dopoledne', 'šesti','šesti_nula_nula', 'šesti_ráno', 'šesti_dopoledne'},
    '6:30' : {'6:30','šest_třicet', 'půl_sedmé_ráno', 'půl_sedmé_dopoledne', 'šesti_třiceti'},
    '7:00' : {'7', '7:00','sedmou', 'sedm', 'sedm_nula_nula', 'sedm_ráno', 'sedm_dopoledne', 'sedmi', 'sedmi_nula_nula', 'sedmi_ráno', 'sedmi_dopoledne'},
    '7:30' : {'7', '7:30','sedm_třicet', 'půl_osmé_ráno', 'půl_osmé_dopoledne', 'sedmi_třiceti'},
    '8:00' : {'8', '8:00','osmou', 'osm', 'osm_nula_nula', 'osm_ráno', 'osm_dopoledne', 'osmi', 'osmi_nula_nula', 'osmi_ráno', 'osmi_dopoledne'},
    '8:30' : {'8:30','osm_třicet', 'půl_deváté_ráno', 'půl_deváté_dopoledne', 'osmi_třiceti'},
    '9:00' : {'9', '9:00','devátou', 'devět', 'devět_nula_nula', 'devět_ráno', 'devět_dopoledne', 'devíti', 'devíti_nula_nula', 'devíti_ráno', 'devíti_dopoledne'},
    '9:30' : {'9:30', 'devět_třicet', 'půl_desáté_ráno', 'půl_desáté_dopoledne', 'devíti_třiceti'},
    '10:00' : {'10', '10:00','desátou', 'deset', 'deset_nula_nula', 'deset_ráno', 'deset_dopoledne', 'deseti', 'deseti_nula_nula', 'deseti_ráno', 'deseti_dopoledne'},
    '10:30' : {'10:30','deset_třicet', 'půl_jedenácté_ráno', 'půl_jedenácté_dopoledne', 'deseti_třiceti'},
    '11:00' : {'11', '11:00','jedenáctou', 'jedenáct', 'jedenáct_nula_nula', 'jedenáct_ráno', 'jedenáct_dopoledne', 'jedenácti', 'jedenácti_nula_nula', 'jedenácti_ráno', 'jedenácti_dopoledne'},
    '11:30' : {'11:30','jedenáct_třicet', 'půl_dvanácté_ráno', 'půl_dvanácté_dopoledne', 'jedenácti_třiceti'},
    '12:00' : {'12', '12:00','dvanáctou', 'dvanáct', 'dvanáct_nula_nula', 'poledne', 'dvanácti', 'dvanácti_nula_nula'},
    '12:30' : {'12:30', 'dvanáct_třicet', 'půl_jedné_odpoledne', 'dvanácti_třiceti'},
    '13:00' : {'13', '13:00','třináctou', 'třináct', 'třináct_nula_nula', 'jedna_odpoledne', 'třinácti', 'třinácti_nula_nula', 'jedné_odpoledne'},
    '13:30' : {'13:30', 'třináct_třicet', 'půl_druhé_odpoledne', 'třinácti_třiceti'},
    '14:00' : {'14', '14:00','čtrnáctou', 'čtrnáct', 'čtrnáct_nula_nula', 'dvě_odpoledne', 'čtrnácti', 'čtrnácti_nula_nula', 'dvou_odpoledne'},
    '14:30' : {'14:30','čtrnáct_třicet', 'půl_třetí_odpoledne', 'čtrnácti_třiceti'},
    '15:00' : {'15', '15:00','patnáctou', 'patnáct', 'patnáct_nula_nula', 'tři_odpoledne', 'patnácti', 'patnácti_nula_nula', 'tří_odpoledne'},
    '15:30' : {'15:30','patnáct_třicet', 'půl_čtvrté_odpoledne', 'patnácti_třiceti'},
    '16:00' : {'16', '16:00','šestnáctou', 'šestnáct', 'šestnáct_nula_nula', 'čtyři_odpoledne', 'šestnácti', 'šestnácti_nula_nula', 'čtyř_odpoledne'},
    '16:30' : {'16:30','šestnáct_třicet', 'půl_páté_odpoledne', 'šestnácti_třiceti'},
    '17:00' : {'17', '17:00','sedmnáctou', 'sedmnáct', 'sedmnáct_nula_nula', 'pět_odpoledne', 'pět_večer', 'sedmnácti', 'sedmnácti_nula_nula', 'pěti_odpoledne', 'pěti_večer'},
    '17:30' : {'17:30','sedmnáct_třicet', 'půl_šesté_odpoledne', 'půl_šesté_večer', 'sedmnácti_třicet'},
    '18:00' : {'18', '18:00','osmnáctou', 'osmnáct', 'osmnáct_nula_nula', 'šest_večer', 'osmnácti', 'osmnácti_nula_nula', 'šesti_večer'},
    '18:30' : {'18:30','osmnáct_třicet', 'půl_sedmé_večer', 'osmnácti_třiceti', 'půl_sedmé_večer'},
    '19:00' : {'19', '19:00','devatenáctou', 'devatenáct', 'devatenáct_nula_nula', 'sedm_večer', 'devatenácti', 'devatenácti_nula_nula', 'sedmi_večer'},
    '19:30' : {'19:30','devatenáct_třicet', 'půl_osmé_večer', 'devatenácti_třiceti', 'půl_osmé_večer'},
    '20:00' : {'20', '20:00','dvacátou', 'dvacet', 'dvacet_nula_nula', 'osm_večer', 'dvaceti', 'dvaceti_nula_nula', 'osmi_večer'}
}

DELKA = {
    '0.5': {'půl_hodiny', 'třicet_minut', '0.5', '0,5', '30'},
    '1': {'hodinu', 'jednu_hodinu', 'šedesát_minut', '1', '60'},
    '1.5': {'hodinu_a_půl', 'jednu_hodinu_a_půl', 'devadesát_minut', '1.5', '1,5', '90'},
    '2': {'dvě_hodiny', '2'},
    '2.5': {'dvě_a_půl_hodiny', '2.5', '2,5'},
    '3': {'tři_hodiny', '3'},
    '3.5': {'tři_a_půl_hodiny', '3.5', '3,5'},
    '4': {'čtyři_hodiny', '4'},
    '4.5': {'čtyři_a_půl_hodiny', '4.5', '4,5'},
    '5': {'pět_hodin', '5'},
    '5.5': {'pět_a_půl_hodiny', '5.5', '5,5'},
    '6': {'šest_hodin', '6'},
    '6.5': {'šest_a_půl_hodiny', '6.5', '6,5'},
    '7': {'sedm_hodin', '7'},
    '7.5': {'sedm_a_půl_hodiny', '7.5', '7,5'},
    '8': {'osm_hodin', '8'},
    '8.5': {'osm_a_půl_hodiny', '8.5', '8,5'},
    '9': {'devět_hodin', '9'},
    '9.5': {'devět_a_půl_hodiny', '9.5', '9,5'},
    '10': {'deset_hodin', '10'},
    '10.5': {'deset_a_půl_hodiny', '10.5', '10,5'},
    '11': {'jedenáct_hodin', '11'},
    '11.5': {'jedenáct_a_půl_hodiny', '11.5', '11,5'},
    '12': {'dvanáct_hodin', 'půl_dne', '12'},
    '24': {'dvacet_čtyři_hodin', 'celý_den', 'celodenní', '24'},
}


POLOZKA = {
    "pečivo": {"pečivo", "pečiva"},
    "šunka": {"šunka", "šunku", "šunky"},
    "sýr": {"sýr", "sýra", "sýry"},
    "těstoviny": {"těstoviny", "těstovin"},
    "rýže": {"rýže", "rýži"},
    "brambory": {"brambory", "brambor"},
    "kuřecí maso": {"kuřecí_maso", "kuřecího_masa", "kuře"},
    "vepřové maso": {"vepřové_maso", "vepřového_masa", "vepřové"},
    "hovězí maso": {"hovězí_maso", "hovězího_masa", "hovězí"},
    "mleté maso": {"mleté_maso", "mletého_masa"},
    "ovesné vločky": {"ovesné_vločky", "ovesných_vloček", "ovesné"},
    "cereálie": {"cereálie", "cereálií"},
    "mléko": {"mléko", "mlíko", "mléka", "mlíka"},
    "vejce": {"vejce", "vajíčka"},
    "chléb": {"chléb", "chleba"},
    "máslo": {"máslo", "másla"},
    "olej": {"olej", "oleje"},
    "jogurt": {"jogurt", "jogurty", "jogurtů"},
    "banán": {"banán", "banány", "banánů"},
    "jablko": {"jablko", "jablka", "jablek"},
    "hruška": {"hruška", "hrušky", "hrušek"},
    "pomeranč": {"pomeranč", "pomeranče", "pomerančů"},
    "citron": {"citron", "citrón", "citrony", "citróny"},
    "okurka": {"okurka", "okurky", "okurek", "okurku"},
    "rajče": {"rajče", "rajčata", "rajčat"},
    "paprika": {"paprika", "papriky", "paprik"},
    "salát": {"salát", "salátu", "saláty"},
    "brokolice": {"brokolice", "brokolici"},
    "květák": {"květák", "květáku"},
    "cuketa": {"cuketa", "cukety", "cuketu"},
    "mrkev": {"mrkev", "mrkve", "mrkví"},
    "cibule": {"cibule", "cibuli", "cibulí"},
    "česnek": {"česnek", "česneku"},
    "chilli": {"chilli", "čili"},
    "rohlík": {"rohlík", "rohlíky", "rohlíků"},
    "sušený salám": {"sušený_salám", "sušeného_salámu"},
    "slanina": {"slanina", "slaniny", "slaninu"},
    "klobása": {"klobása", "klobásy", "klobás"},
    "anglická slanina": {"anglická_slanina", "anglické_slaniny", "anglickou_slaninu"},
    "smetana": {"smetana", "smetany"},
    "tvaroh": {"tvaroh", "tvarohy", "tvarohů"},
    "zmrzlina": {"zmrzlina", "zmrzliny", "zmrzlin"},
    "mouka": {"mouka", "mouky"},
    "cukr": {"cukr", "cukru"},
    "sůl": {"sůl", "soli"},
    "pepř": {"pepř", "pepře"},
    "kmín": {"kmín", "kmínu"},
    "kečup": {"kečup", "kečupu"},
    "hořčice": {"hořčice", "hořčici"},
    "majonéza": {"majonéza", "majonézu"},
    "ocet": {"ocet", "octa"},
    "med": {"med", "medu"},
    "džem": {"džem", "džemu", "džemy"},
    "povidla": {"povidla", "povidel"},
    "čokoláda": {"čokoláda", "čokolády"},
    "minerálka": {"minerálka", "minerálky", "minerálku"},
    "limonáda": {"limonáda", "limonády", "limonádu"},
    "pivo": {"pivo", "piva", "pivu"},
    "víno": {"víno", "vína", "vínu"},
    "rum": {"rum", "rumu"},
    "whisky": {"whisky", "whiskey"},
    "vodka": {"vodka", "vodky"},
    "zelí": {"zelí", "zelím"},
    "špenát": {"špenát", "špenátu"},
    "hrách": {"hrách", "hrachu"},
    "čočka": {"čočka", "čočky"},
    "fazole": {"fazole", "fazolí"},
    "krůtí maso": {"krůtí_maso", "krůtího_masa", "krůta"},
    "jehněčí maso": {"jehněčí_maso", "jehněčího_masa", "jehněčí"},
    "ryba": {"ryba", "ryby", "rybu"},
    "losos": {"losos", "lososa"},
    "tuňák": {"tuňák", "tuňáka"},
    "kapr": {"kapr", "kapra"},
    "ořechy": {"ořechy", "ořechů"},
    "mandle": {"mandle", "mandlí"},
    "rozinky": {"rozinky", "rozinek"},
    "kuskus": {"kuskus", "kuskusu"},
    "bulgur": {"bulgur", "bulguru"},
    "quinoa": {"quinoa", "quinoy"},
    "tofu": {"tofu"},
    "tempeh": {"tempeh", "tempehu"},
    "sójové maso": {"sójové_maso", "sóji"},
    "granola": {"granola", "granoly"},
    "müsli": {"müsli"},
    "pudink": {"pudink", "pudinku"},
    "želatina": {"želatina", "želatiny"},
    "droždí": {"droždí"},
    "prášek do pečiva": {"prášek_do_pečiva", "kypřící_prášek"},
    "vanilkový cukr": {"vanilkový_cukr", "vanilkového_cukru"},
    "skořice": {"skořice"},
    "zázvor": {"zázvor", "zázvoru"},
    "kurkuma": {"kurkuma", "kurkumy"},
    "oregano": {"oregano", "oregana"},
    "bazalka": {"bazalka", "bazalky"},
    "tymián": {"tymián", "tymiánu"},
    "rozmarýn": {"rozmarýn", "rozmarýnu"},
    "bobkový list": {"bobkový_list", "bobkové_listy"},
    "nové koření": {"nové_koření"},
    "hřebíček": {"hřebíček", "hřebíčku"},
    "kardamom": {"kardamom", "kardamomu"},
}

POCET = {
    "1": {'1',"jednakrát", "jedenkrát", "jedno", 'jednou'},
    "2": {'2',"dvě", "dvakrát"},
    "3": {'3',"tři", "třikrát"},  
    "4": {'4',"čtyři", "čtyřikrát"}, 
    "5": {'5',"pět", "pětkrát"},  
    "6": {'6',"šest", "šestkrát"}, 
    "7": {'7',"sedm", "sedmkrát"},  
    "8": {'8',"osm", "osmkrát"}, 
    "9": {'9',"devět", "devětkrát"},  
    "10": {'10',"deset", "desetkrát"},  
}


#TODO: handle different types of schuzka
AKCE = {
    'schůzka' : {'schůzka', 'schůzku'},
    'obecná událost' : {'akce', 'akci', 'událost', 'události'},
    'návštěva doktora' : {'schůzka_u_doktora', 'schůzku_u_doktora', 'doktora', 'doktor'},
    'oběd' : {'oběd', 'schůzku_na_oběd', 'schůzka_na_oběd'},
    'rezervace' : {'rezervace', 'rezervaci'},
    'večeře' : {'večeře', 'schůzka_na_večeři', 'schůzku_na_večeři'},
    'telefonát' : {'telefonát', 'schůzka_po_telefonu', 'schůzku_po_telefonu'},
    'osobní úkol' : {'osobní_úkol', 'úkol'},
    'přednáška' : {'přednáška', 'seminář', 'workshop', 'přednášku'},
    'konference' : {'konference', 'konferenci'},
    'výlet' : {'výlet', 'schůzka_na_výlet', 'schůzku_na_výlet'},
    'narozeniny' : {'narozeniny', 'oslava_narozenin', 'narozeninovou_oslavu'},
    'trénink' : {'trénink', 'tréninkové_schůzku', 'cvičení'},
    'zkouška' : {'zkouška', 'zkoušky', 'zkoušku'},
    'porada' : {'porada', 'poradu'},
    'setkání s přáteli' : {'přátelská_setkání', 'setkání_s_přáteli', 'přátelé', 'přátelské_setkání', 'kamarád', 'přítel'},
    'rodinná událost' : {'rodinná_událost', 'rodinné_setkání', 'rodinnou_oslavu', 'rodina'},
    'mentoring' : {'mentoring', 'mentorování', 'schůzka_s_mentorem'},
}

NAKUP = {
    'nakup' : {'nákup', 'nákupní', 'nákupu', 'nákupního', 'nákupním'},
    'polozka' : {'položka', 'položku', 'položky'}
}

COMMANDS = {
    'akce' : {'naplánováno', 'kalendář', 'kalendáři', 'naplánované', 'naplánovaného', 'plán', 'plánu'},
    'vytvor' : {'vytvoř', 'založ', 'naplánuj', 'přidej', 'vytvořit', 'založit', 'naplánovat', 'přidat'},
    'rekni' : {'co mám', 'řekni', 'jaký', 'jaké', 'co je'},
    'smaz' : {'zruš', 'zrušit', 'smaž', 'smazat', 'odeber', 'odstraň', 'odstranit', 'odebrat'},
    'pomoc': {'pomoc', 'help', 'nápověda', 'nerozumím', 'pomůžeš', 'nevím', 'jak', 'ovládá', 'ovládat'},
    'ano': {'ano', 'jo', 'přeji', 'přeju'},
    'ne': {'ne', 'nepřeji', 'nic', 'nepřeju'},
    'vsechny': {'všechny', 'veškeré', 'každou'},
    # 'aplikace': {'aplikace', 'aplikaci', 'web', 'zůstat', 'zůstaň', 'pozastav', 'pauzuj', 'pauza'},
    'ahoj': {'ahoj', 'zdravím', 'čau', 'čus', 'čest', 'zdar'}
}