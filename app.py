import pandas as pd
import datetime

def csv_to_ofx(input_csv, output_ofx):
    # Charger le fichier CSV
    df = pd.read_csv(input_csv)

    # Convertir la colonne 'date' au format datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # Informations bancaires obligatoires
    bank_id = "30004"  # Code banque
    branch_id = "00628"  # Code guichet
    account_id = "00010267507"  # Numéro de compte

    # Ouvrir le fichier OFX en mode écriture
    with open(output_ofx, 'w') as ofxfile:
        # Écrire l'en-tête OFX
        ofxfile.write("OFXHEADER:100\n")
        ofxfile.write("DATA:OFXSGML\n")
        ofxfile.write("VERSION:102\n")
        ofxfile.write("SECURITY:NONE\n")
        ofxfile.write("ENCODING:USASCII\n")
        ofxfile.write("CHARSET:1252\n")
        ofxfile.write("COMPRESSION:NONE\n")
        ofxfile.write("OLDFILEUID:NONE\n")
        ofxfile.write("NEWFILEUID:NONE\n\n")

        # Écrire le contenu OFX
        ofxfile.write("<OFX>\n")
        ofxfile.write("  <SIGNONMSGSRSV1>\n")
        ofxfile.write("    <SONRS>\n")
        ofxfile.write("      <STATUS>\n")
        ofxfile.write("        <CODE>0\n")
        ofxfile.write("        <SEVERITY>INFO\n")
        ofxfile.write("      </STATUS>\n")
        ofxfile.write("      <DTSERVER>20250101\n")
        ofxfile.write("      <LANGUAGE>FRA\n")
        ofxfile.write("    </SONRS>\n")
        ofxfile.write("  </SIGNONMSGSRSV1>\n")
        ofxfile.write("  <BANKMSGSRSV1>\n")
        ofxfile.write("    <STMTTRNRS>\n")
        ofxfile.write("      <TRNUID>0\n")
        ofxfile.write("      <STATUS>\n")
        ofxfile.write("        <CODE>0\n")
        ofxfile.write("        <SEVERITY>INFO\n")
        ofxfile.write("      </STATUS>\n")
        ofxfile.write("      <STMTRS>\n")
        ofxfile.write("        <CURDEF>EUR\n")
        ofxfile.write(f"        <BANKACCTFROM>\n")
        ofxfile.write(f"          <BANKID>{bank_id}</BANKID>\n")
        ofxfile.write(f"          <BRANCHID>{branch_id}</BRANCHID>\n")
        ofxfile.write(f"          <ACCTID>{account_id}</ACCTID>\n")
        ofxfile.write("          <ACCTTYPE>CHECKING\n")
        ofxfile.write("        </BANKACCTFROM>\n")
        ofxfile.write("        <BANKTRANLIST>\n")

        for index, row in df.iterrows():
            # Déterminer le type de transaction (CREDIT ou DEBIT)
            trn_type = 'CREDIT' if row['amount'] > 0 else 'DEBIT'
            amount = abs(row['amount'])
            date_posted = row['date'].strftime('%Y%m%d')

            # Écrire la transaction dans le fichier OFX
            ofxfile.write("          <STMTTRN>\n")
            ofxfile.write(f"            <TRNTYPE>{trn_type}\n")
            ofxfile.write(f"            <DTPOSTED>{date_posted}\n")
            ofxfile.write(f"            <TRNAMT>{amount:.2f}\n")
            ofxfile.write(f"            <NAME>{row['reference']}\n")
            ofxfile.write("          </STMTTRN>\n")

        ofxfile.write("        </BANKTRANLIST>\n")
        ofxfile.write("      </STMTRS>\n")
        ofxfile.write("    </STMTTRNRS>\n")
        ofxfile.write("  </BANKMSGSRSV1>\n")
        ofxfile.write("</OFX>\n")

    print(f"Conversion terminée : {output_ofx} créé avec succès.")


