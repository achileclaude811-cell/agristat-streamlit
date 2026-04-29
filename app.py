import streamlit as st
import pandas as pd
import sqlite3
import statistics
from datetime import date
import os

st.set_page_config(page_title="AgriStat Pro 🐄", page_icon="🐄", layout="wide")

st.markdown("""
<style>
.stApp{background-color:#0d1f17;color:#e8f5ee}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d2b1a,#122a1e);border-right:2px solid #2d5c44}
[data-testid="stSidebar"] *{color:#e8f5ee!important}
h1,h2{color:#4ade80!important}h3{color:#86efac!important}
[data-testid="metric-container"]{background:#1a3a28;border:1px solid #2d5c44;border-top:3px solid #4ade80;border-radius:12px;padding:12px}
[data-testid="metric-container"] label{color:#9dc4ad!important;font-size:11px!important}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#e8f5ee!important}
.stButton>button{background:#4ade80!important;color:#0d1f17!important;font-weight:700!important;border-radius:8px!important;border:none!important}
.stButton>button:hover{background:#22c55e!important}
.stDownloadButton>button{background:#f59e0b!important;color:#0d1f17!important;font-weight:700!important;border-radius:8px!important;border:none!important}
.stTabs [data-baseweb="tab-list"]{background:#122a1e;border-radius:8px}
.stTabs [data-baseweb="tab"]{color:#9dc4ad!important}
.stTabs [aria-selected="true"]{background:#4ade80!important;color:#0d1f17!important;border-radius:6px}
.streamlit-expanderHeader{background:#1a3a28!important;color:#4ade80!important;border-radius:8px!important}
.streamlit-expanderContent{background:#122a1e!important;border:1px solid #2d5c44!important}
hr{border-color:#2d5c44!important}
</style>
""", unsafe_allow_html=True)

# ── Base de données ───────────────────────────────────────────────────────────
DB = "agristat.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS fiches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_collecte TEXT, nom_eleveur TEXT, localite TEXT, region TEXT,
        espece TEXT, systeme_elevage TEXT, effectif_total INTEGER DEFAULT 0,
        effectif_males INTEGER DEFAULT 0, effectif_femelles INTEGER DEFAULT 0,
        age_moyen REAL DEFAULT 0, poids_moyen REAL DEFAULT 0, etat_sante TEXT,
        taux_mortalite REAL DEFAULT 0, production_journaliere REAL DEFAULT 0,
        alimentation TEXT, superficie_m2 REAL DEFAULT 0,
        vaccination INTEGER DEFAULT 0, type_vaccin TEXT, maladies TEXT,
        cout_mensuel REAL DEFAULT 0, revenu_mensuel REAL DEFAULT 0,
        observations TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit(); conn.close()

def get_all():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM fiches ORDER BY date_collecte DESC", conn)
    conn.close(); return df

def insert_fiche(data):
    conn = sqlite3.connect(DB)
    conn.execute("""INSERT INTO fiches (date_collecte,nom_eleveur,localite,region,
        espece,systeme_elevage,effectif_total,effectif_males,effectif_femelles,
        age_moyen,poids_moyen,etat_sante,taux_mortalite,production_journaliere,
        alimentation,superficie_m2,vaccination,type_vaccin,maladies,
        cout_mensuel,revenu_mensuel,observations) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
    conn.commit(); conn.close()

def delete_fiche(fid):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM fiches WHERE id=?", (fid,))
    conn.commit(); conn.close()

init_db()

# ── Données démo ──────────────────────────────────────────────────────────────
def seed():
    if len(get_all()) == 0:
        demo = [
            ("2026-04-01","Jean-Pierre Mballa","Mimboman","Centre","Poulet","Intensif",500,120,380,3.5,1.8,"Bon",2.5,320,"Aliment complet",200,1,"Newcastle","",75000,180000,"Bon élevage"),
            ("2026-04-02","Marie Ateba","Obala","Centre","Canard","Semi-Intensif",200,60,140,5.0,2.4,"Excellent",1.0,90,"Son de blé",150,1,"Influenza","",40000,120000,"Très bon"),
            ("2026-04-03","Paul Essomba","Soa","Centre","Porc","Semi-Intensif",80,20,60,8.0,65.0,"Bon",3.0,0,"Déchets+provende",300,1,"Rouget","Gale",90000,250000,"Traitement en cours"),
            ("2026-04-05","Cécile Ngo","Yaoundé","Centre","Caille","Intensif",1200,400,800,2.0,0.18,"Excellent",0.5,700,"Aliment caille",80,0,"","",35000,140000,"Excellente production"),
            ("2026-04-07","Thomas Nkoa","Mbalmayo","Centre","Ovin","Extensif",45,15,30,18.0,28.0,"Moyen",5.0,0,"Pâturage",5000,0,"","Parasites",8000,60000,"Déparasitage requis"),
            ("2026-04-10","Suzanne Fouda","Douala","Littoral","Poulet","Intensif",2000,200,1800,4.0,2.1,"Bon",1.8,1400,"Aliment ponte",600,1,"Newcastle+Marek","",280000,700000,"Grande exploitation"),
            ("2026-04-12","Alain Beyala","Bafoussam","Ouest","Lapin","Intensif",300,100,200,4.0,2.8,"Bon",4.0,0,"Herbes+aliment",120,1,"Myxomatose","",25000,90000,"Reproduction régulière"),
            ("2026-04-15","Hélène Manga","Garoua","Nord","Bovin","Extensif",120,30,90,36.0,320.0,"Excellent",0.8,180,"Pâturage",50000,1,"PPCB","",150000,600000,"Troupeau Goudali"),
            ("2026-04-18","Roger Eto'o","Ngaoundéré","Adamaoua","Caprin","Extensif",85,20,65,14.0,22.0,"Moyen",6.0,25,"Pâturage",8000,0,"","PPR",5000,45000,"Consultation urgente"),
            ("2026-04-20","Christine Owono","Ebolowa","Sud","Dinde","Semi-Intensif",150,40,110,6.0,7.5,"Bon",3.5,60,"Maïs+son",400,1,"Newcastle","",55000,180000,"Bonne croissance"),
            ("2026-04-22","Fabrice Ndzana","Bertoua","Est","Poulet","Extensif",80,30,50,5.0,1.5,"Moyen",8.0,30,"Maïs",500,0,"","Bronchite",12000,35000,"Amélioration requise"),
            ("2026-04-25","Nadège Tchoua","Kribi","Sud","Pigeon","Semi-Intensif",500,250,250,8.0,0.45,"Excellent",0.5,40,"Grains",60,0,"","",18000,75000,"Pigeons voyageurs"),
        ]
        for d in demo: insert_fiche(d)
seed()

ESPECES  = ["Poulet","Canard","Dinde","Lapin","Porc","Bovin","Ovin","Caprin","Caille","Pigeon","Autre"]
SYSTEMES = ["Intensif","Semi-Intensif","Extensif"]
SANTES   = ["Excellent","Bon","Moyen","Mauvais"]
REGIONS  = ["Adamaoua","Centre","Est","Extrême-Nord","Littoral","Nord","Nord-Ouest","Ouest","Sud","Sud-Ouest"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:16px 0'><div style='font-size:48px'>🐄</div><div style='font-size:20px;font-weight:700;color:#4ade80'>AgriStat Pro</div><div style='font-size:11px;color:#9dc4ad;text-transform:uppercase;letter-spacing:1px'>Collecte & Analyse Élevage</div></div>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("", ["📊 Tableau de bord","➕ Nouvelle collecte","📋 Données collectées","🔬 Analyse descriptive","📥 Exporter"], label_visibility="collapsed")
    st.divider()
    df_s = get_all()
    st.markdown(f"<div style='text-align:center;font-size:12px;color:#9dc4ad'><b style='color:#4ade80'>{len(df_s)}</b> fiches | <b style='color:#f59e0b'>{int(df_s['effectif_total'].sum()) if not df_s.empty else 0:,}</b> animaux</div>", unsafe_allow_html=True)
    st.divider()
    st.caption("📚 INF232 EC2 — Université de Yaoundé I")
    st.caption("🐍 Python · Streamlit · SQLite")

# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Tableau de bord":
    st.title("📊 Tableau de Bord")
    st.caption("Vue d'ensemble en temps réel des données d'élevage")
    st.divider()
    df = get_all()
    if df.empty:
        st.warning("🐣 Aucune donnée. Ajoutez une fiche de collecte.")
        st.stop()

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("📋 Fiches",          len(df))
    c2.metric("🐓 Animaux",         f"{int(df['effectif_total'].sum()):,}")
    c3.metric("⚖️ Poids moy.",      f"{df['poids_moyen'].mean():.1f} kg")
    c4.metric("💀 Mortalité moy.",  f"{df['taux_mortalite'].mean():.1f}%")
    c5.metric("🥚 Production moy.", f"{df['production_journaliere'].mean():.0f}/j")
    c6.metric("💉 Vaccinés",        f"{int(df['vaccination'].sum())}/{len(df)}")
    st.divider()

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### 🐓 Fiches par espèce")
        esp = df["espece"].value_counts().reset_index(); esp.columns=["Espèce","Fiches"]
        st.bar_chart(esp.set_index("Espèce"), color="#4ade80", height=250)
    with col2:
        st.markdown("#### 🏥 État de santé")
        san = df["etat_sante"].value_counts().reset_index(); san.columns=["Santé","Nombre"]
        st.bar_chart(san.set_index("Santé"), color="#38bdf8", height=250)

    col3,col4 = st.columns(2)
    with col3:
        st.markdown("#### 💀 Mortalité par espèce (%)")
        mort = df.groupby("espece")["taux_mortalite"].mean().reset_index(); mort.columns=["Espèce","Mortalité(%)"]
        st.bar_chart(mort.set_index("Espèce"), color="#f87171", height=250)
    with col4:
        st.markdown("#### 🌍 Effectif par région")
        reg = df.groupby("region")["effectif_total"].sum().reset_index(); reg.columns=["Région","Effectif"]
        st.bar_chart(reg.set_index("Région"), color="#f59e0b", height=250)

    col5,col6 = st.columns(2)
    with col5:
        st.markdown("#### 💰 Revenu vs Coût par espèce (FCFA)")
        eco = df.groupby("espece")[["cout_mensuel","revenu_mensuel"]].mean().round(0)
        eco.columns=["Coût moyen","Revenu moyen"]
        st.bar_chart(eco, height=250)
    with col6:
        st.markdown("#### 🔵 Poids ↔ Production")
        sc = df[["poids_moyen","production_journaliere"]].copy()
        sc.columns=["Poids (kg)","Production/j"]
        st.scatter_chart(sc, x="Poids (kg)", y="Production/j", height=250)

    st.divider()
    st.markdown("#### 🕐 Dernières fiches collectées")
    st.dataframe(df[["date_collecte","nom_eleveur","localite","espece","effectif_total","etat_sante","taux_mortalite"]].head(10).rename(columns={"date_collecte":"Date","nom_eleveur":"Éleveur","localite":"Localité","espece":"Espèce","effectif_total":"Effectif","etat_sante":"Santé","taux_mortalite":"Mortalité%"}), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Nouvelle collecte":
    st.title("➕ Nouvelle Fiche de Collecte")
    st.caption("Renseignez toutes les informations sur l'exploitation animale")
    st.divider()

    with st.form("form_collecte", clear_on_submit=True):
        st.markdown("### 🗓️ Identification")
        c1,c2 = st.columns(2)
        date_collecte = c1.date_input("📅 Date de collecte *", value=date.today())
        nom_eleveur   = c2.text_input("👤 Nom de l'éleveur *", placeholder="Nom complet")
        c3,c4 = st.columns(2)
        localite = c3.text_input("📍 Localité / Village *", placeholder="Ex: Mimboman")
        region   = c4.selectbox("🗺️ Région", REGIONS)
        st.divider()

        st.markdown("### 🐓 Espèce & Effectif")
        c1,c2 = st.columns(2)
        espece          = c1.selectbox("🦎 Espèce animale *", ESPECES)
        systeme_elevage = c2.selectbox("🏠 Système d'élevage", SYSTEMES)
        c3,c4,c5 = st.columns(3)
        effectif_total    = c3.number_input("📦 Effectif total *", min_value=0, value=0)
        effectif_males    = c4.number_input("♂️ Dont mâles",       min_value=0, value=0)
        effectif_femelles = c5.number_input("♀️ Dont femelles",    min_value=0, value=0)
        superficie_m2 = st.number_input("📐 Superficie du parc (m²)", min_value=0.0, value=0.0, step=10.0)
        st.divider()

        st.markdown("### ⚖️ Paramètres Zootechniques")
        c1,c2,c3 = st.columns(3)
        age_moyen   = c1.number_input("📅 Âge moyen (mois)",  min_value=0.0, value=0.0, step=0.5)
        poids_moyen = c2.number_input("⚖️ Poids moyen (kg)",  min_value=0.0, value=0.0, step=0.1)
        etat_sante  = c3.selectbox("🏥 État de santé", SANTES)
        c4,c5 = st.columns(2)
        taux_mortalite         = c4.number_input("💀 Taux mortalité (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        production_journaliere = c5.number_input("🥚 Production journalière", min_value=0.0, value=0.0)
        alimentation = st.text_input("🌽 Type d'alimentation", placeholder="Ex: Maïs, Son de blé, Aliment complet...")
        st.divider()

        st.markdown("### 💉 Santé & Prévention")
        c1,c2 = st.columns(2)
        vaccination = c1.checkbox("✅ Vaccination effectuée ?")
        type_vaccin = c2.text_input("💊 Type de vaccin", placeholder="Ex: Newcastle, Gumboro...")
        maladies = st.text_input("🦠 Maladies / Symptômes", placeholder="Ex: Bronchite, Gale, Parasites...")
        st.divider()

        st.markdown("### 💰 Données Économiques")
        c1,c2 = st.columns(2)
        cout_mensuel   = c1.number_input("💸 Coût alimentation/mois (FCFA)", min_value=0.0, value=0.0, step=1000.0)
        revenu_mensuel = c2.number_input("💵 Revenu mensuel estimé (FCFA)",  min_value=0.0, value=0.0, step=1000.0)
        observations = st.text_area("📝 Observations", height=80, placeholder="Remarques, recommandations...")
        st.divider()

        submitted = st.form_submit_button("💾 Enregistrer la fiche", use_container_width=True)
        if submitted:
            if not nom_eleveur.strip() or not localite.strip() or effectif_total == 0:
                st.error("❌ Remplissez les champs obligatoires (*) : nom, localité, effectif")
            else:
                insert_fiche((str(date_collecte),nom_eleveur.strip(),localite.strip(),region,
                    espece,systeme_elevage,effectif_total,effectif_males,effectif_femelles,
                    age_moyen,poids_moyen,etat_sante,taux_mortalite,production_journaliere,
                    alimentation,superficie_m2,int(vaccination),type_vaccin,maladies,
                    cout_mensuel,revenu_mensuel,observations))
                st.success("✅ Fiche enregistrée avec succès !")
                st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Données collectées":
    st.title("📋 Données Collectées")
    st.divider()
    df = get_all()
    if df.empty:
        st.warning("Aucune fiche enregistrée."); st.stop()

    st.markdown("#### 🔍 Filtres")
    c1,c2,c3,c4 = st.columns(4)
    fe = c1.selectbox("Espèce",    ["Toutes"]+ESPECES)
    fs = c2.selectbox("Santé",     ["Tous"]  +SANTES)
    fr = c3.selectbox("Région",    ["Toutes"]+REGIONS)
    fv = c4.selectbox("Vaccination",["Tous","Oui","Non"])

    df_f = df.copy()
    if fe != "Toutes": df_f = df_f[df_f["espece"]==fe]
    if fs != "Tous":   df_f = df_f[df_f["etat_sante"]==fs]
    if fr != "Toutes": df_f = df_f[df_f["region"]==fr]
    if fv == "Oui":    df_f = df_f[df_f["vaccination"]==1]
    if fv == "Non":    df_f = df_f[df_f["vaccination"]==0]

    st.caption(f"**{len(df_f)}** fiche(s) sur {len(df)} au total")
    st.dataframe(df_f[["id","date_collecte","nom_eleveur","localite","region","espece","effectif_total","poids_moyen","etat_sante","taux_mortalite","vaccination"]].rename(columns={"id":"ID","date_collecte":"Date","nom_eleveur":"Éleveur","localite":"Localité","region":"Région","espece":"Espèce","effectif_total":"Effectif","poids_moyen":"Poids(kg)","etat_sante":"Santé","taux_mortalite":"Mortalité%","vaccination":"Vacciné"}), use_container_width=True, hide_index=True, height=350)
    st.divider()

    st.markdown("#### 🔎 Détail d'une fiche")
    c_id, c_act = st.columns([2,1])
    fid    = c_id.number_input("ID de la fiche", min_value=1, step=1, value=1)
    action = c_act.radio("Action", ["👁️ Voir","🗑️ Supprimer"], horizontal=True)
    row = df[df["id"]==fid]

    if not row.empty:
        r = row.iloc[0]
        if action == "👁️ Voir":
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("👤 Éleveur",    r["nom_eleveur"])
            c2.metric("📍 Localité",   f"{r['localite']}, {r['region']}")
            c3.metric("🐓 Espèce",     r["espece"])
            c4.metric("📅 Date",       r["date_collecte"])
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("📦 Effectif",   f"{r['effectif_total']} animaux")
            c2.metric("⚖️ Poids",      f"{r['poids_moyen']} kg")
            c3.metric("🏥 Santé",      r["etat_sante"])
            c4.metric("💀 Mortalité",  f"{r['taux_mortalite']}%")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("🥚 Production", f"{r['production_journaliere']}/j")
            c2.metric("💉 Vacciné",    "Oui" if r["vaccination"] else "Non")
            c3.metric("💸 Coût/mois",  f"{r['cout_mensuel']:,.0f} FCFA")
            c4.metric("💵 Revenu",     f"{r['revenu_mensuel']:,.0f} FCFA")
            if r["cout_mensuel"] > 0:
                rent = (r["revenu_mensuel"]-r["cout_mensuel"])/r["cout_mensuel"]*100
                if rent > 0: st.success(f"📈 Rentabilité : **+{rent:.1f}%** — Élevage rentable")
                else: st.error(f"📉 Rentabilité : **{rent:.1f}%** — Élevage déficitaire")
            if r["maladies"]: st.warning(f"🦠 Maladies : {r['maladies']}")
            if r["observations"]: st.info(f"📝 {r['observations']}")
        else:
            st.error(f"⚠️ Supprimer la fiche #{int(fid)} de **{r['nom_eleveur']}** ?")
            if st.button("🗑️ Confirmer"):
                delete_fiche(int(fid)); st.success("Supprimée !"); st.rerun()
    else:
        st.warning(f"Aucune fiche avec l'ID {fid}")

# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔬 Analyse descriptive":
    st.title("🔬 Analyse Descriptive")
    st.caption("Statistiques calculées automatiquement sur toutes les données collectées")
    st.divider()
    df = get_all()
    if df.empty:
        st.warning("Aucune donnée à analyser."); st.stop()

    st.info(f"📊 **{len(df)} fiches** — {int(df['effectif_total'].sum()):,} animaux recensés")

    def stat_desc(col, unite=""):
        vals = df[col].dropna().tolist()
        if not vals: return None
        moy = round(statistics.mean(vals),2)
        med = round(statistics.median(vals),2)
        ety = round(statistics.stdev(vals),2) if len(vals)>1 else 0
        return {"N":len(vals),"Minimum":f"{round(min(vals),2)} {unite}","Maximum":f"{round(max(vals),2)} {unite}","Moyenne":f"{moy} {unite}","Médiane":f"{med} {unite}","Écart-type":f"{ety} {unite}","Étendue":f"{round(max(vals)-min(vals),2)} {unite}","Variance":f"{round(ety**2,2)}"}

    tab1,tab2,tab3,tab4 = st.tabs(["📊 Stats univariées","🔀 Tableaux croisés","🔵 Corrélations","📋 Résumé global"])

    with tab1:
        st.markdown("#### Indicateurs statistiques par variable quantitative")
        variables = [
            ("effectif_total","📦 Effectif total","animaux"),
            ("poids_moyen","⚖️ Poids moyen","kg"),
            ("taux_mortalite","💀 Taux mortalité","%"),
            ("production_journaliere","🥚 Production journalière","unités"),
            ("age_moyen","📅 Âge moyen","mois"),
            ("superficie_m2","📐 Superficie","m²"),
            ("cout_mensuel","💸 Coût alimentation","FCFA"),
            ("revenu_mensuel","💵 Revenu mensuel","FCFA"),
        ]
        for col,label,unite in variables:
            s = stat_desc(col, unite)
            if s:
                with st.expander(label):
                    c1,c2,c3,c4 = st.columns(4)
                    c1.metric("N",           s["N"])
                    c2.metric("Moyenne",     s["Moyenne"])
                    c3.metric("Médiane",     s["Médiane"])
                    c4.metric("Écart-type",  s["Écart-type"])
                    c1.metric("Minimum",     s["Minimum"])
                    c2.metric("Maximum",     s["Maximum"])
                    c3.metric("Étendue",     s["Étendue"])
                    c4.metric("Variance",    s["Variance"])
                    st.bar_chart(df[col].dropna().value_counts().sort_index(), height=120)

    with tab2:
        st.markdown("#### Espèce × État de santé")
        st.dataframe(pd.crosstab(df["espece"],df["etat_sante"],margins=True,margins_name="TOTAL"), use_container_width=True)
        st.divider()
        st.markdown("#### Région × Espèce")
        st.dataframe(pd.crosstab(df["region"],df["espece"],margins=True,margins_name="TOTAL"), use_container_width=True)
        st.divider()
        st.markdown("#### Système d'élevage × Vaccination")
        df["vacc_label"] = df["vaccination"].map({1:"Oui",0:"Non"})
        st.dataframe(pd.crosstab(df["systeme_elevage"],df["vacc_label"]), use_container_width=True)

    with tab3:
        st.markdown("#### 🔵 Poids ↔ Production")
        sc1 = df[["poids_moyen","production_journaliere"]].copy(); sc1.columns=["Poids (kg)","Production/j"]
        st.scatter_chart(sc1, x="Poids (kg)", y="Production/j", height=280)
        st.markdown("#### 🔵 Effectif ↔ Revenu mensuel")
        sc2 = df[["effectif_total","revenu_mensuel"]].copy(); sc2.columns=["Effectif","Revenu (FCFA)"]
        st.scatter_chart(sc2, x="Effectif", y="Revenu (FCFA)", height=280)
        st.markdown("#### 🔗 Matrice de corrélation")
        num = ["effectif_total","poids_moyen","taux_mortalite","production_journaliere","age_moyen","cout_mensuel","revenu_mensuel"]
        corr = df[num].corr().round(3)
        corr.columns = corr.index = ["Effectif","Poids","Mortalité","Production","Âge","Coût","Revenu"]
        st.dataframe(corr, use_container_width=True)

    with tab4:
        st.markdown("#### Résumé statistique complet (describe)")
        num = ["effectif_total","poids_moyen","taux_mortalite","production_journaliere","age_moyen","cout_mensuel","revenu_mensuel"]
        res = df[num].describe().round(2)
        res.index = ["N","Moyenne","Écart-type","Minimum","Q1(25%)","Médiane","Q3(75%)","Maximum"]
        res.columns = ["Effectif","Poids(kg)","Mortalité(%)","Production/j","Âge(mois)","Coût(FCFA)","Revenu(FCFA)"]
        st.dataframe(res, use_container_width=True)
        st.divider()
        st.markdown("#### Synthèse par espèce")
        synth = df.groupby("espece").agg(Fiches=("id","count"),Effectif=("effectif_total","sum"),Poids_Moy=("poids_moyen","mean"),Mortalite_Moy=("taux_mortalite","mean"),Production_Moy=("production_journaliere","mean"),Revenu_Moy=("revenu_mensuel","mean")).round(2)
        st.dataframe(synth, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif page == "📥 Exporter les données":
    st.title("📥 Exporter les Données")
    st.divider()
    df = get_all()
    if df.empty:
        st.warning("Aucune donnée à exporter."); st.stop()

    st.success(f"✅ **{len(df)} fiche(s)** — {int(df['effectif_total'].sum()):,} animaux")
    st.divider()

    df_exp = df.drop(columns=["created_at"]).rename(columns={
        "id":"ID","date_collecte":"Date","nom_eleveur":"Éleveur","localite":"Localité",
        "region":"Région","espece":"Espèce","systeme_elevage":"Système",
        "effectif_total":"Effectif Total","effectif_males":"Mâles","effectif_femelles":"Femelles",
        "age_moyen":"Âge(mois)","poids_moyen":"Poids(kg)","etat_sante":"Santé",
        "taux_mortalite":"Mortalité(%)","production_journaliere":"Production/j",
        "alimentation":"Alimentation","superficie_m2":"Superficie(m²)",
        "vaccination":"Vacciné","type_vaccin":"Vaccin","maladies":"Maladies",
        "cout_mensuel":"Coût(FCFA)","revenu_mensuel":"Revenu(FCFA)","observations":"Observations"
    })

    c1,c2 = st.columns(2)
    c1.download_button("📥 Télécharger CSV (Excel)", df_exp.to_csv(index=False,encoding="utf-8-sig"),
        f"agristat_{date.today()}.csv","text/csv", use_container_width=True)
    c2.download_button("📥 Télécharger JSON", df_exp.to_json(orient="records",force_ascii=False,indent=2),
        f"agristat_{date.today()}.json","application/json", use_container_width=True)

    st.divider()
    st.markdown("#### Aperçu des données")
    st.dataframe(df_exp, use_container_width=True, hide_index=True)
