import sqlite3
from datetime import date

def create_connection():
        sqliteConnection = sqlite3.connect('kaffedb.db')
        cursor = sqliteConnection.cursor()
        print("Database successfully Connected to SQLite")
        sqlite_select_Query = """SELECT * FROM bruker"""
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print(record)
        
        status = input(str("Vil du logge inn (1) eller registrere deg (2)? "))
        if status == "1":
            bruker_epost = input(str("Tast inn epostadresse: "))
            passord = input(str("tast inn passord: "))
            
            
        else:
            bruker_epost = input(str("Tast inn din epostadresse: "))
            navn = input(str("Skriv inn fullt navn: "))
            passord = input(str("Tast inn ditt passord: "))
            sql = """INSERT INTO bruker (epost, navn, passord) VALUES(?, ?, ?)"""
            cursor.execute(sql, (bruker_epost, navn, passord))
            sqliteConnection.commit()
            create_connection()
    
        autenticate = False
        sqlite_select_Query = """SELECT * FROM bruker WHERE epost =? AND passord =?"""
        cursor.execute(sqlite_select_Query, (bruker_epost, passord))
        record = cursor.fetchall()
        print(record)
        if len(record) > 0:
            print(len(record))
            autenticate = True

        else:
            cursor.close()
            print("Feil passord/epost")
            create_connection()

               
        if autenticate:


            
            brukerhistorie = input(str("Hvilken brukerhistorie vil du teste? (Velg enten 1,2,3,4,5): "))
            
            if brukerhistorie == "1":
                print("Registrer ny kaffesmaking")
                kaffenavn = input(str("Skriv inn navnet på kaffen du smakte: "))
                print("Dette er brenneriene du kan velge mellom: ")
                brenneri = input(str("Skriv inn kaffens brenneri: "))
                poeng = input("Gi en poengscore fra 1-10: ") 
                smaksnotat = input(str("Skriv inn ditt smaksnotat: "))
                smaksdato = str(date.today())
                
                query = """INSERT INTO kaffesmaking(smaksnotat, smaksdato, poeng, bruker_epost, 
                kaffenavn) VALUES(?,?, ?, ?, ?);"""
                cursor.execute(query, (smaksnotat, smaksdato, poeng, bruker_epost, kaffenavn))
                sqliteConnection.commit()
                print("Kaffesmaking registrert!")
            
            
            elif brukerhistorie == "2":
                smaksdato = input(str("For hvilket årstall vil du sjekke listen over hvilke brukere som har smakt flest unike kaffer?: "))
                sqlite_select_Query =   f"""select bruker.navn, COUNT(*) as "antall kaffesmakinger" from kaffesmaking inner join bruker on kaffesmaking.bruker_epost = bruker.epost
                                            WHERE kaffesmaking.smaksdato LIKE '%{smaksdato}%'
                                            group by bruker.navn ORDER BY COUNT(*) DESC; """
                cursor.execute(sqlite_select_Query)
                records = cursor.fetchall()
                print(records)

            
            elif brukerhistorie == "3":
                print("Finner hvilke kaffer som gir mest for pengene:")
                sqlite_select_Query =   f"""SELECT brentkaffe.brennerinavn, brentkaffe.kaffenavn, brentkaffe.kilopris_nok,avg(poeng) from brentkaffe 
                                        inner join kaffesmaking on kaffesmaking.kaffenavn = brentkaffe.kaffenavn
                                        group by brentkaffe.kaffenavn
                                        ORDER BY poeng DESC;
                                        """
                cursor.execute(sqlite_select_Query)
                records = cursor.fetchall()
                print(records)

                
            elif brukerhistorie == "4":
                print("Finner florale kaffer:")
                sqlite_select_Query =   f"""SELECT DISTINCT brentkaffe.brennerinavn, brentkaffe.kaffenavn FROM brentkaffe INNER JOIN kaffesmaking ON brentkaffe.kaffenavn = kaffesmaking.kaffenavn
                WHERE brentkaffe.beskrivelse LIKE '%floral%' or kaffesmaking.smaksnotat LIKE '%floral%';"""
                cursor.execute(sqlite_select_Query)
                records = cursor.fetchall()
                print(records)

            
            elif brukerhistorie == "5":
                print("Finner uvaskede kaffer fra Rwanda og Colombia:")
                sqlite_select_Query =   f"""SELECT brentkaffe.brennerinavn, brentkaffe.kaffenavn FROM brentkaffe inner JOIN kaffeparti
                ON brentkaffe.partiId = kaffeparti.partiId
                JOIN gard on gard.gardsnavn = kaffeparti.gardsnavn
                WHERE kaffeparti.metode <> "vasket" and (gard.land = 'Rwanda' or gard.land = 'Colombia');
                """
                cursor.execute(sqlite_select_Query)
                records = cursor.fetchall()
                print(records)

        cursor.close()     

create_connection()


