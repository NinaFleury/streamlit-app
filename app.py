import pandas as pd
import datetime
import streamlit as st

# Titre de l'application
st.title("Convertisseur CSV vers OFX")

# Champs pour les informations bancaires obligatoires
bank_id = st.text_input("Entrez le code banque (BANKID)", "30004")
branch_id = st.text_input("Entrez le code guichet (BRANCHID)", "00628")
account_id = st.text_input("Entrez le numéro de compte (ACCTID)", "00010267507")

# Téléversement du fichier CSV
uploaded_file = st.file_uploader("Téléversez un fichier CSV (colonnes : Date, Reference, Amount)", type=["csv"])

if uploaded_file is not None:
    try:
        # Charger le fichier CSV
        df = pd.read_csv(uploaded_file)

        # Convertir la colonne 'Date' au format datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

        # Nom du fichier OFX de sortie
        output_ofx = "output.ofx"

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
                trn_type = 'CREDIT' if row['Amount'] > 0 else 'DEBIT'
                amount = abs(row['Amount'])
                date_posted = row['Date'].strftime('%Y%m%d')

                # Écrire la transaction dans le fichier OFX
                ofxfile.write("          <STMTTRN>\n")
                ofxfile.write(f"            <TRNTYPE>{trn_type}\n")
                ofxfile.write(f"            <DTPOSTED>{date_posted}\n")
                ofxfile.write(f"            <TRNAMT>{amount:.2f}\n")
                ofxfile.write(f"            <NAME>{row['Reference']}\n")
                ofxfile.write("          </STMTTRN>\n")

            ofxfile.write("        </BANKTRANLIST>\n")
            ofxfile.write("      </STMTRS>\n")
            ofxfile.write("    </STMTTRNRS>\n")
            ofxfile.write("  </BANKMSGSRSV1>\n")
            ofxfile.write("</OFX>\n")

        # Proposer le téléchargement du fichier OFX
        st.success("Conversion terminée ! Téléchargez votre fichier OFX ci-dessous :")
        with open(output_ofx, "rb") as ofx_download:
            st.download_button("Télécharger le fichier OFX", ofx_download, file_name=output_ofx)

    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
