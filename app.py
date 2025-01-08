import streamlit as st
import pandas as pd
import datetime

def transactions_to_ofx(df, output_file):
    # Convertir les colonnes Debit et Credit en nombres
    df['Debit'] = df['Debit'].fillna(0).str.replace(',', '.').astype(float)
    df['Credit'] = df['Credit'].fillna(0).str.replace(',', '.').astype(float)

    # Créer le contenu OFX
    with open(output_file, 'w') as f:
        f.write("OFXHEADER:100\n")
        f.write("DATA:OFXSGML\n")
        f.write("VERSION:102\n")
        f.write("SECURITY:NONE\n")
        f.write("ENCODING:USASCII\n")
        f.write("CHARSET:1252\n")
        f.write("COMPRESSION:NONE\n")
        f.write("OLDFILEUID:NONE\n")
        f.write("NEWFILEUID:NONE\n\n")
        f.write("<OFX>\n")
        f.write("  <SIGNONMSGSRSV1>\n")
        f.write("    <SONRS>\n")
        f.write("      <STATUS>\n")
        f.write("        <CODE>0\n")
        f.write("        <SEVERITY>INFO\n")
        f.write("      </STATUS>\n")
        f.write("      <DTSERVER>20250101\n")
        f.write("      <LANGUAGE>FRA\n")
        f.write("    </SONRS>\n")
        f.write("  </SIGNONMSGSRSV1>\n")
        f.write("  <BANKMSGSRSV1>\n")
        f.write("    <STMTTRNRS>\n")
        f.write("      <TRNUID>0\n")
        f.write("      <STATUS>\n")
        f.write("        <CODE>0\n")
        f.write("        <SEVERITY>INFO\n")
        f.write("      </STATUS>\n")
        f.write("      <STMTRS>\n")
        f.write("        <CURDEF>EUR\n")
        f.write("        <BANKTRANLIST>\n")

        for _, row in df.iterrows():
            amount = row['Credit'] if row['Credit'] > 0 else -row['Debit']
            date_posted = datetime.datetime.strptime(row['Date'], '%d/%m/%Y').strftime('%Y%m%d')

            f.write("          <STMTTRN>\n")
            f.write(f"            <TRNTYPE>{'CREDIT' if amount > 0 else 'DEBIT'}\n")
            f.write(f"            <DTPOSTED>{date_posted}\n")
            f.write(f"            <TRNAMT>{amount:.2f}\n")
            f.write(f"            <NAME>{row['Description']}\n")
            f.write("          </STMTTRN>\n")

        f.write("        </BANKTRANLIST>\n")
        f.write("      </STMTRS>\n")
        f.write("    </STMTTRNRS>\n")
        f.write("  </BANKMSGSRSV1>\n")
        f.write("</OFX>\n")

    return output_file

# Interface utilisateur avec Streamlit
st.title("Convertisseur CSV vers OFX")

uploaded_file = st.file_uploader("Téléversez un fichier CSV (colonnes : Date, Description, Debit, Credit)", type=["csv"])

if uploaded_file:
    # Charger les données avec gestion des erreurs d'encodage
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        st.warning("Erreur d'encodage détectée. Tentative avec l'encodage 'latin1'...")
        df = pd.read_csv(uploaded_file, encoding='latin1')

    output_file = "output.ofx"
    transactions_to_ofx(df, output_file)

    # Proposer le téléchargement
    st.success("Conversion terminée ! Téléchargez votre fichier :")
    with open(output_file, "rb") as f:
        st.download_button("Télécharger le fichier OFX", f, file_name="output.ofx")
