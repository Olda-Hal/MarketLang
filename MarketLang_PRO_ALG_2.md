# Programování na Akciovém trhu
Organizátoři ZISKu začali obchodovat s akciemi a velmi je to začalo bavit. Nastal ale problém. Obchodování s akciemi jim zabírá moc času a tak už nestíhají jejich oblíbené programování. Rozhodli se proto že tyto dvě činnosti spojí.
Po dlouhé práci vytvořili nový programovací jazyk, který je revoluční v tom, že pro zavolání jakékoli instrukce je potřeba ji prvně zakoupit z burzy. Ceny na burze se pořád mění, a proto je potřeba nakupovat ve správný okamžik.
Stejně tak můžete prodávat instrukce, které už nepotřebujete. Ale pozor, ceny se mění a můžete prodávat se ztrátou.
Další místo kde se orgové rozhodli zapojit je obchod s nemovitostmi, proto každé místo v paměti je potřeba pronajmout a platit za něj.

# MarketLang
Tento nový revoluční jazyk se jmenuje MarketLang a je založen na následujících principech:
- Každá instrukce je potřeba zakoupit na burze
- Každá instrukce má svou cenu
- Ceny se mění
- Instrukce lze prodávat
- Místa v paměti je potřeba pronajmout

# Instrukce
Tento programovací jazyk poskytuje následující instrukce:

## Neplacené instrukce
- `PRICE <instrukce>` - zjistí cenu instrukce
- `BUY <instrukce>` - koupí instrukci
- `SELL <instrukce>` - prodá instrukci
- `COUNT <instrukce>` - zjistí počet zakoupených instrukcí
- `WALLET` - zjistí počet peněz v peněžence
- `WAIT` - počká jeden takt akciového trhu
- `PRINT <instrukce>` - vytiskne instrukci 

## Placené instrukce
(TODO) - vytvořit seznam instrukcí


# Zadání úlohy
Při spuštění kódu dostanete 10000 peněz v peněžence. Vaším úkolem bude vytvořit interpreter BrainFucku (TODO: vymyslet jestli tohle je dobry zadani???) v programovacím jazyce MarketLang. Důležité ale je udělat program tak aby ideálně na konci běhu zůstal v profitu nebo aspoň nastejno jak začal.

## Hodnocení
Bodování budete podle toho kolik peněz vám zůstane po doběhnutí několika různých programů. Výsledně to bude ohodnocené následující tabulkou:

|% Puvodních peněz| Počet bodů|
|-|-|
|90%+|10|
|80-89%|9|
|70-79%|8|
|60-69%|7|
|50-59%|6|
|40-49%|5|
|30-39%|4|
|20-29%|3|
|10-19%|2|
|0-9%|1|

(TODO): zjistit jestli je hodnocení smysluplné?




