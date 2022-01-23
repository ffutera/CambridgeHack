import pandas as pd 
from model import Investment

# Global constants
numeric_columns = ['Total Environmental Cost', 'Working Capacity', 'Fish Production Capacity', 'Crop Production Capacity', 'Meat Production Capacity',
                     'Biodiversity', 'Abiotic Resources', 'Water production capacity (Drinking water & Irrigation Water)', 'Wood Production Capacity']

# Read and process data
investment_df=pd.read_csv("data/final_raw_sample_0_percent.csv")
investment_df = investment_df.replace(',','', regex=True)
for col in numeric_columns:
    investment_df[col] = investment_df[col].map(lambda x: x[1:-1])
    investment_df = investment_df[investment_df[col] != ""]
    investment_df = investment_df[investment_df[col] != " "]
    investment_df[col] = investment_df[col].astype('int')

# Main algorithm
def computeRank(i): # Value of i decides if something is to be returned or not 
    global investment_df
    ranking_columns = ['Total Environmental Cost', 'Working Capacity', 'Fish Production Capacity', 'Crop Production Capacity', 'Meat Production Capacity','Biodiversity', 'Abiotic Resources', 'Water production capacity (Drinking water & Irrigation Water)', 'Wood Production Capacity']
    bin_investment_df = investment_df.copy(deep=True)
    for col in ranking_columns:
        if(col=="Total Environmental Cost"):
            bin_investment_df[col] = 4*pd.qcut(investment_df[col].rank(method='first'), 4, labels=False)
        elif(col=="Biodiversity"):
            bin_investment_df[col] = 2*pd.qcut(investment_df[col].rank(method='first'), 4, labels=False)
        else:
            bin_investment_df[col] = pd.qcut(investment_df[col].rank(method='first'), 4, labels=False)
    investment_df['mean'] = bin_investment_df.iloc[:, 6:13].mean(axis=1)
    if(i):
        return bin_investment_df

        
def addInvestment(investment_descriptor):
    global investment_df
    investment = {'Company Name': investment_descriptor.company_name,
                  'Country': investment_descriptor.country,
                  'Total Environmental Cost': investment_descriptor.total_env_cost,
                  'Working Capacity': investment_descriptor.work_capacity, 
                  'Fish Production Capacity': investment_descriptor.fish_prod_capacity, 
                  'Crop Production Capacity': investment_descriptor.crop_prod_capacity, 
                  'Meat Production Capacity': investment_descriptor.meat_prod_capacity,
                  'Biodiversity': investment_descriptor.biodiversity, 
                  'Abiotic Resources': investment_descriptor.abio_rescs, 
                  'Water production capacity (Drinking water & Irrigation Water)': investment_descriptor.water_prod_capacity, 
                  'Wood Production Capacity': investment_descriptor.wood_prod_capacity}
    investment_df = investment_df.append(investment, ignore_index = True)
    # compute rank with new company
    computeRank(False)
    
        
def investmentClassifier(investment_descriptor):
    global investment_df
    # add unknown company
    if not investment_df['Company Name'].isin([investment_descriptor.company_name]).any() and not investment_df['Year'].isin([investment_descriptor.country]).any():
        addInvestment(investment_descriptor)
    # find rank of input company
    company_rank = investment_df[investment_df['Company Name'] == investment_descriptor.company_name]['mean'].mean()
    rounded_company_rank = round(company_rank)
    rounded_company_rank = 1 if rounded_company_rank < 1 else 4 if rounded_company_rank > 4 else rounded_company_rank
    return rounded_company_rank

#Calculate initial means for topFive
dummy_run = Investment('dude test company', 'Switzerland', 55143243, 0, 11456, 646758, 0, 2061, 3661, 5828063, 4)
investmentClassifier(dummy_run)

# Get most sustainable firms
def topFive():
    global investment_df
    calculation=investment_df
    top= calculation[calculation["mean"]==1].head()
    return zip(top["Company Name"],top["Country"])

# Get suggestions for better firms
def getSuggestions(curr_rank):
    global investment_df 
    possible_upgrades_df = investment_df[round(investment_df['mean']) < curr_rank]
    possible_upgrades = []

    if not possible_upgrades_df.empty: # there are better options
        possible_upgrades_df = possible_upgrades_df.sample(n=3)
        possible_upgrades = possible_upgrades_df['Company Name'].tolist()
        return possible_upgrades
    else: # smallest possible bin - so best we can do is same level
        possible_upgrades_df = investment_df[investment_df['mean'] == curr_rank]
        possible_upgrades_df = possible_upgrades_df.sample(n=3)
        possible_upgrades = possible_upgrades_df['Company Name'].tolist()
        return possible_upgrades

# Get summarizing descriptions
def good_parameters(investment_descriptor):
    parameters=[]
    ranking_columns = ['Total Environmental Cost', 'Working Capacity', 'Fish Production Capacity', 'Crop Production Capacity', 'Meat Production Capacity','Biodiversity', 'Abiotic Resources', 'Water production capacity (Drinking water & Irrigation Water)', 'Wood Production Capacity']
    i=0
    bin_investment_df=computeRank(True)
    for companies in bin_investment_df["Company Name"]:
        for col in ranking_columns:
            if(companies==investment_descriptor.company_name):
                if(col=="Total Environmental Cost" and int(bin_investment_df[bin_investment_df["Company Name"]==companies][col])<4):
                    parameters.append(col)
                    i+=1
                elif(col=="Biodiversity" and int(bin_investment_df[bin_investment_df["Company Name"]==companies][col])<2):
                    parameters.append(col)
                    i+=1
                elif(int(bin_investment_df[bin_investment_df["Company Name"]==companies][col])<1):
                    parameters.append(col)
                    i+=1
                if(i==3):
                    good=parameters
                    parameters=[]
                    return good
        
def bad_parameters(investment_descriptor):
    parameters=[]
    ranking_columns = ['Total Environmental Cost', 'Working Capacity', 'Fish Production Capacity', 'Crop Production Capacity', 'Meat Production Capacity','Biodiversity', 'Abiotic Resources', 'Water production capacity (Drinking water & Irrigation Water)', 'Wood Production Capacity']
    i=0
    bin_investment_df=computeRank(True)
    for companies in bin_investment_df["Company Name"]:
        for col in ranking_columns:
            if(companies==investment_descriptor.company_name):
                if(col=="Total Environmental Cost" and int(bin_investment_df[bin_investment_df["Company Name"]==companies][col])>=12):
                    parameters.append(col)
                    i+=1
                elif(col=="Biodiversity" and int(bin_investment_df[bin_investment_df["Company Name"]==companies][col])>=6):
                    parameters.append(col)
                    i+=1
                elif(int(bin_investment_df[bin_investment_df["Company Name"]==companies][col])>=3):
                    parameters.append(col)
                    i+=1
                if(i==3):
                    bad=parameters
                    parameters=[]
                    return bad