import pandas as pd
import numpy as np

df = pd.read_excel("C:/Users/Michel.LAPTOP-16TFAQA2/Documents/Michel/Insper/Entidades/Insper Data/Marketing 2022.1/Base_selenium2.xlsx")

df.rename(columns = {'Num de Aval':'Volume'}, inplace = True)
df.drop(df.columns[0], axis = 1, inplace = True)
df.replace("[]",np.nan, inplace = True)
df = df.dropna(how = 'any').reset_index(drop = True)
df.head()


df.to_excel("C:/Users/Michel.LAPTOP-16TFAQA2/Documents/Michel/Insper/Entidades/Insper Data/Marketing 2022.1/Base_selenium3.xlsx")




























