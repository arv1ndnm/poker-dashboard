import streamlit as st 
# from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import altair as alt
# import plotly.express as px


from datetime import datetime


# url = 'https://docs.google.com/spreadsheets/d/1kPFvghQfYSWU8uudqYCJAq9dhKoLejnSnDUGm8a-7Mg/edit?pli=1&gid=0#gid=0&fvid=1352800863'

# url = 'https://docs.google.com/spreadsheets/d/1kPFvghQfYSWU8uudqYCJAq9dhKoLejnSnDUGm8a-7Mg/edit?usp=sharing'

# conn = st.connection("gsheets", type=GSheetsConnection)

# data = conn.read(spreadsheet=url, usecols=[0, 1])
# st.dataframe(data)

st.set_page_config(
    page_title="Poker Stats",
    # page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


df = pd.read_csv('Poker Stats - Data.csv')
player = ""
month = ""
with st.sidebar:
    st.title('Poker Dashboard')
    
    player = st.selectbox('Select a player',df['Player Name'].sort_values().unique(), index=None)

    month = st.selectbox('Select a month', df[df['Player Name'] == player]['Month'].sort_values().unique(), index=None,)
    
    # selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    # df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    # color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)



# .....NEED TO TACKLE THIS DATE FORMAT AT THE SOURCE...

df['Date'] = df['Date'].astype(str) + "/2024"
df['Date'] = pd.to_datetime(pd.Series(df['Date']), format = "%d/%m/%Y")

# Now you want to filter for players within the selected team. 
# index=None so that it doesn't default to any player. 'index=0' will default to the first player on the list
# player = st.selectbox('Select a player', df[df['team'] == team]['player'].sort_values().unique(), index=None) 


def filter_data(df, player, month):
    if player:
        df = df[df['Player Name'] == player]
        if month == None:
            df = df
        else:
            df = df[df['Month'] == month]
    return df

filtered_df  = filter_data(df, player, month)
player_net = filtered_df['Net Gain/Loss'].sum()
sessions_played = filtered_df['Player Name'].count()
tot_buy_in = filtered_df['Buy-In Amount'].sum()
tot_takeaway = filtered_df['Final Takeaway'].sum()
win_perc = np.round(filtered_df['Net Gain/Loss'].gt(0).sum()/sessions_played*100,2)
loss_perc = np.round(filtered_df['Net Gain/Loss'].lt(0).sum()/sessions_played*100,2)
draw_perc = np.round((filtered_df['Net Gain/Loss']==0).sum()/sessions_played*100,2)
avg_buy = np.round(tot_buy_in/sessions_played,2)
avg_take = tot_takeaway/sessions_played
avg_net = np.round(player_net/sessions_played,2)


st.write(filtered_df)

try:
    st.write(player + f" has played {sessions_played} game(s) in total.")
    if(player_net > 0):
        st.write(player + f"'s NET :green[Gain]/:red[Loss]: :green[{player_net}↑]")
    else:
        st.write(player + f"'s NET :green[Gain]/:red[Loss]: :red[{player_net}↓]")

    if sessions_played >= 5:
        if(avg_net > 0):
            st.write(player + f"'s AVERAGE :green[Gain]/:red[Loss]: :green[{avg_net}↑] with an average buy-in of {avg_buy}. (+{np.round(avg_net/avg_buy*100,2)}%)")
        else:
            st.write(player + f"'s AVERAGE :green[Gain]/:red[Loss]: :red[{avg_net}↓] with an average buy-in of {avg_buy}. (-{np.round(avg_net/avg_buy*100,2)}%)")        
    else:
        
        if(avg_net > 0):
            st.write(player + f"'s AVERAGE :green[Gain]/:red[Loss]: :green[{avg_net}↑] with an average buy-in of {avg_buy}. (+{np.round(avg_net/avg_buy*100,2)}%). :red[WARNING]: Played less than 5 games. Average is not representational.")
        else:
            st.write(player + f"'s AVERAGE :green[Gain]/:red[Loss]: :red[{avg_net}↓] with an average buy-in of {avg_buy}. (-{np.round(avg_net/avg_buy*100,2)}%). :red[WARNING]: Played less than 5 games. Average is not representational.")
        # st.markdown(f" :red[WARNING]: Played less than 5 games. Average is not representational.")


except Exception as exc:
    Exception(exc)

# Initialize data to lists
percentae_table = [{'Win %': win_perc, 'Draw %': draw_perc, 'Loss %': loss_perc}]
perc_df = pd.DataFrame(percentae_table)

st.table(perc_df)

# st.write(f" Win percentage: {win_perc}%")
# st.write(f" Loss percentage: {loss_perc}%")
# st.write(f" Draw percentage: {draw_perc}%")

labels = player , 'Remaining players'
sizes = [filtered_df['Final Takeaway'].sum(), df['Final Takeaway'].sum()]
explode = (0.15, 0,)  
fig1, ax1 = plt.subplots(1,1)



if(player!=""):
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=180)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set_title('Percentage of total winnings')
    st.pyplot(fig1)


# filtered_df.plot(x="Date", y=["Net Gain/Loss"],
#         kind="line", figsize=(10, 10))
# # plt.plot(filtered_df['Date'], filtered_df['Net Gain/Loss'])
# plt.show()
