# LU07.A01 - Wikipedia Path to Philosophy

## E2E-Test mit TestCafé

Dieser Test automatisiert das "Wikipedia Path to Philosophy" Phänomen.

## Installation

TestCafé ist bereits installiert.

## Test ausführen

```bash
# Einmal ausführen
npm run test:wikipedia

# Oder mehrmals um die längste Kette zu finden
for i in {1..10}; do
  echo "Run #$i:"
  npm run test:wikipedia
  echo "---"
done
```

## Der Test

Der Test:
1. Öffnet eine zufällige Wikipedia-Seite
2. Klickt den ersten gültigen Link (ausgenommen: italic, sup, infobox)
3. Merkt sich besuchte Seiten
4. Wiederholt bis "Philosophy" erreicht wird oder eine Schleife erkannt wird
5. Protokolliert die Kette

## Ergebnis

Führen Sie den Test mehrmals aus und notieren Sie:
- Die längste gefundene Kette
- Der Begriff mit der längsten Kette

Geben Sie den Begriff mit der längsten Kette auf Moodle ein.

## Implementierung

Siehe [`wikipedia-path-to-philosophy.test.ts`](wikipedia-path-to-philosophy.test.ts)
