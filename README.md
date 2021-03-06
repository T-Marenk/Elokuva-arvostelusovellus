# Elokuva-arvostelusovellus

## Tietoa projektista

Nettisovellus, jossa pääsee antamaan arvioita elokuvista

Projekti on tehty Helsingin yliopiston kurssia _Aineopintojen harjoitustyö: Tietokantasovellus_ varten

## Lopullinen sovellus

Sovelluksessa on seuraavat toiminnot:

- Käyttäjän luominen ja sisään kirjautuminen
- Elokuvien hakeminen sivulta nimen tai genren mukaan
- Arvosteluiden jättäminen
- Elokuvilla on omat sivut
- Ylläpitäjä toiminnot
	- Elokuvien lisääminen
	- Kommenttien poisto
	- Elokuva pyyntöjen näkeminen
	- Uuden katselualustan lisääminen sovellukseen
	- Elokuvien poistaminen
	- Elokuvalle uuden katsomisalustan lisääminen
- Elokuva pyyntöjen jättäminen
- Elokuvalla näkee, millä alustalla sen voi katsoa

Sovelluksessa on siis kaikki alunperin sille suunnitellut toiminnallisuudet. Näkymien välillä pääsee kulkemaan sivuston sisäisillä linkeillä ja jokaisesta näkymästä pääsee helposti palaamaan etusivulle. Normaaleille käyttäjille olevissa tekstikentissä on mahdolliset tarkistukset tiedon oikeallisuudesta, esimerkiksi vuosiluvun tarkistetaan olevan vuosiluku. Ylläpitäjä toiminnot ovat toiminnallisia vain ylläpitäjille eikä niille pääse ilman ylläpitäjän oikeuksia.

## Heroku

Sovellus on toiminnassa herokussa osoitteessa [https://popcorn-arvostelut.herokuapp.com/](https://popcorn-arvostelut.herokuapp.com/). 

Sovellukseen on lisätty valmiiksi yksi käyttäjä, joka on ylläpitäjä, jolla pääsee testaamaan sivun kaikkia toimintoja. Tämän käyttäjän käyttäjänimi on admin ja salasana on A1234. Tämä käyttäjä on tarpeellinen, jos haluaa päästä testaamaan ylläpitäjille tarkoitettuja toimintoja. Lisäksi sovelluksessa on joitain elokuvia lisättynä testaamista varten.

## Muokkaaminen ja oma käyttö

Mikäli tahdot muokata sovellusta tai ottaa sen omaan käyttöösi herokun ulkopuolelta, lataa sovelluksen lähdekoodi _zip_-tiedostona, kloona se koneellesi tai forkkaa se. 

Ennen sovellukseen käyttöön ottoa asenna riippuvuudet koneellesi suorittamalla

```bash
pip install -r requirements.txt
```
Suorittaaksesi sovellus paikallisesti tulee olla virtuaaliympäristössä. Tähän pääsee suorittamalla juurihakemistossa

```bash
source venv/bin/activate
```

Sovellus käyttää PostgreSQL -tietokantaa. Sovelluksen toimintaa varten tulee siis olla asennettuna PostgreSQL, jonka tulee olla käynnistettynä sovellusta suorittaessa.

Tarvittavat taulukot saa kopioitua omaan tietokantaan suorittamalla

```bash
psql < schema.sql
```

sovelluksen juurihakemistossa

## Alkuperäinen suunnitelma sovelluksen ominaisuuksista

- Henkilö pystyy luomaan itsellensä käyttäjän ja kirjautua sisään

- Jokaisella elokuvalla on oma sivunsa

- Käyttäjät voivat antaa elokuville arvosteluita

- Sovelluksesta voi hakea elokuvia nimen tai genren perusteella

- Ylläpitäjä voi lisätä elokuvan sovellukseen tai poistaa elokuvan sovelluksesta

- Ylläpitäjä voi poistaa käyttäjän arvostelun

- Käyttäjä voi jättää sovellukseen pyynnön elokuvasta, jonka haluaa lisättäväksi sovellukseen

- Elokuviin voi lisätä tiedon paikasta, jossa sen voi katsoa


