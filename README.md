# Immuni TEK (Telegram) sender
Questo piccolo progetto controlla se sul server di Immuni sono stati aggiunti dei nuovi batch
di chiavi di infetti da COVID-19 e in quel caso li invia su un 
[canale Telegram](https://t.me/immunikeys) dedicato.
Tutto il codice rilasciato in questo progetto è da considerarsi software libero con
esclusione del file `src/protobuild/exposurekey.proto` sotto 
[copyright](https://developers.google.com/terms/site-policies) di Google.

## Motivazioni
Il progetto è stato creato per rendere il più trasparente possibile l'aggiunta di nuove
chiavi di infetti sul server di Immuni. 
Inoltre, è risaputo che alcune versioni di Android bloccano il servizio periodico 
di reperimento chiavi di Immuni; questo canale Telegram può quindi essere un aiuto
per ricordare ai possessori di tali dispositivi di aprire l'app regolarmente per controllare
la corrispondenza di chiavi di infetti. 
La curiosità tecnica dell'autore sull'infrastuttura dell'app Immuni è stato un altro
importante fattore.

## Deployment
Per deployare il progetto, si consiglia di installare i `requirements.txt` dentro un 
virtualenv di Python3 e di impostare crontab per eseguire lo script `main.py` ogni
tot minuti.
