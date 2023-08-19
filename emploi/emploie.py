import pandas as pd

def calculeActifParDep():

    file_path = 'estim-pop-dep-sexe-gca-1975-2023.xls'
    df2017 = pd.read_excel(file_path,"2017",skiprows=3, header=[0, 1], nrows=96)
    df2022 = pd.read_excel(file_path,"2022",skiprows=3, header=[0, 1], nrows=96)

    subset_columns = [('Départements', 'Unnamed: 0_level_1'),
                            ('Départements', 'Unnamed: 1_level_1'),
                            ('Ensemble', '20 à 39 ans'),
                            ('Ensemble', '40 à 59 ans')]


    df2022=df2022[subset_columns]
    df2017=df2017[subset_columns]

    df2017 = df2017.assign(Total_Actif=df2017[('Ensemble', '20 à 39 ans')] + df2017[('Ensemble', '40 à 59 ans')])
    df2022 = df2022.assign(Total_Actif=df2022[('Ensemble', '20 à 39 ans')] + df2022[('Ensemble', '40 à 59 ans')])

    df2017.drop(columns=[('Ensemble', '20 à 39 ans'), ('Ensemble', '40 à 59 ans')], inplace=True)
    df2022.drop(columns=[('Ensemble', '20 à 39 ans'), ('Ensemble', '40 à 59 ans')], inplace=True)

    
    df2022['Départements_fusionnes'] = df2022.apply(fusionner_departements, axis=1)

    df2022.drop(columns=[('Départements', 'Unnamed: 0_level_1'), ('Départements', 'Unnamed: 1_level_1')], inplace=True)

    df2017['Départements_fusionnes'] = df2017.apply(fusionner_departements, axis=1)

    df2017.drop(columns=[('Départements', 'Unnamed: 0_level_1'), ('Départements', 'Unnamed: 1_level_1')], inplace=True)

    departements_inclus = ['89', '21', '71', '58']

    df2017_filtered = df2017[df2017['Départements_fusionnes'].str[:2].isin(departements_inclus)]
    df2022_filtered = df2022[df2022['Départements_fusionnes'].str[:2].isin(departements_inclus)]
    return fusionner_dataframe(df2017_filtered,df2022_filtered)


def fusionner_dataframe(df_2017, df_2022):

    df_2017['Mois'] = 2017
    df_2022['Mois'] = 2022

    merged_df = pd.concat([df_2017, df_2022])

    pivot_df = merged_df.pivot(index='Mois', columns='Départements_fusionnes', values='Total_Actif')

    pivot_df.reset_index(inplace=True)

    pivot_df.columns.name = None

    new_columns = ['Mois'] + [f'{col.split(" ")[-1]} {col.split(" ")[0]}' for col in pivot_df.columns[1:]]
    pivot_df.columns = new_columns
    return pivot_df



def fusionner_departements(row):
    departement1 = row[('Départements', 'Unnamed: 0_level_1')]
    departement2 = row[('Départements', 'Unnamed: 1_level_1')]
    return f"{departement1} {departement2}"

def calculeMoyenneDemandeurParAnParDep():
    data = pd.read_csv('Demandeur_Emploie.csv', skiprows=3, delimiter=';', nrows=330)
    annee = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"]

    nouvelles_colonnes = {}
    for colonne in data.columns[:-1]:  
        nouvelles_colonnes[colonne] = []

    df = pd.DataFrame(nouvelles_colonnes)

    df['Mois'] = annee

    for col in data.columns[1:-1]:
        listeMoyenne=[]
        cpt = 1
        moyenne = 0
        for valeur in data[col]:
            moyenne += int(valeur.replace(" ", ""))
            if(cpt%12==0):
                listeMoyenne.append(moyenne//12)
                moyenne=0
            if(data.iloc[(cpt-1),0]=="Juin 2023"):
                listeMoyenne.append(moyenne//6)
            cpt+=1
        df[col]=listeMoyenne

    colonnes_desirees = ["Mois", "Côte-d'Or 21", "Yonne 89", "Nièvre 58", "Saône-et-Loire 71"]
    df = df[colonnes_desirees]

    annees_desirees = ["2017", "2022"]
    df = df[df['Mois'].isin(annees_desirees)]

    df = df.reset_index(drop=True)

    sorted_columns = ['Mois'] + sorted(df.columns[1:], key=extract_dept_number)
    df_sorted = df[sorted_columns]
    return df_sorted

def extract_dept_number(column_name):
    return int(column_name.split()[-1])

def indicateurParDep(df_2017,df_2022):
    df_2017_values = df_2017.drop(columns='Mois')
    df_2022_values = df_2022.drop(columns='Mois')

    result_values = df_2022_values.divide(df_2017_values)
    result_values = result_values*100

    result_df = pd.concat([df_2022['Mois'], result_values], axis=1)
    print(result_df)
    return result_df

df1 = calculeActifParDep()
df2 = calculeMoyenneDemandeurParAnParDep()
print(df1)
print(df2)
final = indicateurParDep(df1,df2)
