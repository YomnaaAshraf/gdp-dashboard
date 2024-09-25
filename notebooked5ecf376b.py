{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "_cell_guid": "b1076dfc-b9ad-4769-8c92-a6c4dae69d19",
    "_uuid": "8f2839f25d086af736a60e9eeb907d3b93b6e0e5",
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:24.020748Z",
     "iopub.status.busy": "2024-09-25T09:05:24.020331Z",
     "iopub.status.idle": "2024-09-25T09:05:25.047931Z",
     "shell.execute_reply": "2024-09-25T09:05:25.046985Z",
     "shell.execute_reply.started": "2024-09-25T09:05:24.020707Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/kaggle/input/zomato-bangalore-restaurants/zomato.csv\n"
     ]
    }
   ],
   "source": [
    "# This Python 3 environment comes with many helpful analytics libraries installed\n",
    "# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python\n",
    "# For example, here's several helpful packages to load\n",
    "\n",
    "import numpy as np # linear algebra\n",
    "import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\n",
    "from sklearn.compose import ColumnTransformer\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n",
    "from sklearn.impute import SimpleImputer\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.ensemble import RandomForestClassifier\n",
    "from sklearn.model_selection import cross_validate\n",
    "# Input data files are available in the read-only \"../input/\" directory\n",
    "# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory\n",
    "\n",
    "import os\n",
    "for dirname, _, filenames in os.walk('/kaggle/input'):\n",
    "    for filename in filenames:\n",
    "        print(os.path.join(dirname, filename))\n",
    "\n",
    "# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using \"Save & Run All\" \n",
    "# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:25.050153Z",
     "iopub.status.busy": "2024-09-25T09:05:25.049724Z",
     "iopub.status.idle": "2024-09-25T09:05:30.259348Z",
     "shell.execute_reply": "2024-09-25T09:05:30.258442Z",
     "shell.execute_reply.started": "2024-09-25T09:05:25.050119Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>url</th>\n",
       "      <th>address</th>\n",
       "      <th>name</th>\n",
       "      <th>online_order</th>\n",
       "      <th>book_table</th>\n",
       "      <th>rate</th>\n",
       "      <th>votes</th>\n",
       "      <th>phone</th>\n",
       "      <th>location</th>\n",
       "      <th>rest_type</th>\n",
       "      <th>dish_liked</th>\n",
       "      <th>cuisines</th>\n",
       "      <th>approx_cost(for two people)</th>\n",
       "      <th>reviews_list</th>\n",
       "      <th>menu_item</th>\n",
       "      <th>listed_in(type)</th>\n",
       "      <th>listed_in(city)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>https://www.zomato.com/bangalore/jalsa-banasha...</td>\n",
       "      <td>942, 21st Main Road, 2nd Stage, Banashankari, ...</td>\n",
       "      <td>Jalsa</td>\n",
       "      <td>Yes</td>\n",
       "      <td>Yes</td>\n",
       "      <td>4.1/5</td>\n",
       "      <td>775</td>\n",
       "      <td>080 42297555\\r\\n+91 9743772233</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Casual Dining</td>\n",
       "      <td>Pasta, Lunch Buffet, Masala Papad, Paneer Laja...</td>\n",
       "      <td>North Indian, Mughlai, Chinese</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  A beautiful place to ...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>https://www.zomato.com/bangalore/spice-elephan...</td>\n",
       "      <td>2nd Floor, 80 Feet Road, Near Big Bazaar, 6th ...</td>\n",
       "      <td>Spice Elephant</td>\n",
       "      <td>Yes</td>\n",
       "      <td>No</td>\n",
       "      <td>4.1/5</td>\n",
       "      <td>787</td>\n",
       "      <td>080 41714161</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Casual Dining</td>\n",
       "      <td>Momos, Lunch Buffet, Chocolate Nirvana, Thai G...</td>\n",
       "      <td>Chinese, North Indian, Thai</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  Had been here for din...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>https://www.zomato.com/SanchurroBangalore?cont...</td>\n",
       "      <td>1112, Next to KIMS Medical College, 17th Cross...</td>\n",
       "      <td>San Churro Cafe</td>\n",
       "      <td>Yes</td>\n",
       "      <td>No</td>\n",
       "      <td>3.8/5</td>\n",
       "      <td>918</td>\n",
       "      <td>+91 9663487993</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Cafe, Casual Dining</td>\n",
       "      <td>Churros, Cannelloni, Minestrone Soup, Hot Choc...</td>\n",
       "      <td>Cafe, Mexican, Italian</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 3.0', \"RATED\\n  Ambience is not that ...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>https://www.zomato.com/bangalore/addhuri-udupi...</td>\n",
       "      <td>1st Floor, Annakuteera, 3rd Stage, Banashankar...</td>\n",
       "      <td>Addhuri Udupi Bhojana</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>3.7/5</td>\n",
       "      <td>88</td>\n",
       "      <td>+91 9620009302</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Quick Bites</td>\n",
       "      <td>Masala Dosa</td>\n",
       "      <td>South Indian, North Indian</td>\n",
       "      <td>300</td>\n",
       "      <td>[('Rated 4.0', \"RATED\\n  Great food and proper...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>https://www.zomato.com/bangalore/grand-village...</td>\n",
       "      <td>10, 3rd Floor, Lakshmi Associates, Gandhi Baza...</td>\n",
       "      <td>Grand Village</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>3.8/5</td>\n",
       "      <td>166</td>\n",
       "      <td>+91 8026612447\\r\\n+91 9901210005</td>\n",
       "      <td>Basavanagudi</td>\n",
       "      <td>Casual Dining</td>\n",
       "      <td>Panipuri, Gol Gappe</td>\n",
       "      <td>North Indian, Rajasthani</td>\n",
       "      <td>600</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  Very good restaurant ...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                 url  \\\n",
       "0  https://www.zomato.com/bangalore/jalsa-banasha...   \n",
       "1  https://www.zomato.com/bangalore/spice-elephan...   \n",
       "2  https://www.zomato.com/SanchurroBangalore?cont...   \n",
       "3  https://www.zomato.com/bangalore/addhuri-udupi...   \n",
       "4  https://www.zomato.com/bangalore/grand-village...   \n",
       "\n",
       "                                             address                   name  \\\n",
       "0  942, 21st Main Road, 2nd Stage, Banashankari, ...                  Jalsa   \n",
       "1  2nd Floor, 80 Feet Road, Near Big Bazaar, 6th ...         Spice Elephant   \n",
       "2  1112, Next to KIMS Medical College, 17th Cross...        San Churro Cafe   \n",
       "3  1st Floor, Annakuteera, 3rd Stage, Banashankar...  Addhuri Udupi Bhojana   \n",
       "4  10, 3rd Floor, Lakshmi Associates, Gandhi Baza...          Grand Village   \n",
       "\n",
       "  online_order book_table   rate  votes                             phone  \\\n",
       "0          Yes        Yes  4.1/5    775    080 42297555\\r\\n+91 9743772233   \n",
       "1          Yes         No  4.1/5    787                      080 41714161   \n",
       "2          Yes         No  3.8/5    918                    +91 9663487993   \n",
       "3           No         No  3.7/5     88                    +91 9620009302   \n",
       "4           No         No  3.8/5    166  +91 8026612447\\r\\n+91 9901210005   \n",
       "\n",
       "       location            rest_type  \\\n",
       "0  Banashankari        Casual Dining   \n",
       "1  Banashankari        Casual Dining   \n",
       "2  Banashankari  Cafe, Casual Dining   \n",
       "3  Banashankari          Quick Bites   \n",
       "4  Basavanagudi        Casual Dining   \n",
       "\n",
       "                                          dish_liked  \\\n",
       "0  Pasta, Lunch Buffet, Masala Papad, Paneer Laja...   \n",
       "1  Momos, Lunch Buffet, Chocolate Nirvana, Thai G...   \n",
       "2  Churros, Cannelloni, Minestrone Soup, Hot Choc...   \n",
       "3                                        Masala Dosa   \n",
       "4                                Panipuri, Gol Gappe   \n",
       "\n",
       "                         cuisines approx_cost(for two people)  \\\n",
       "0  North Indian, Mughlai, Chinese                         800   \n",
       "1     Chinese, North Indian, Thai                         800   \n",
       "2          Cafe, Mexican, Italian                         800   \n",
       "3      South Indian, North Indian                         300   \n",
       "4        North Indian, Rajasthani                         600   \n",
       "\n",
       "                                        reviews_list menu_item  \\\n",
       "0  [('Rated 4.0', 'RATED\\n  A beautiful place to ...        []   \n",
       "1  [('Rated 4.0', 'RATED\\n  Had been here for din...        []   \n",
       "2  [('Rated 3.0', \"RATED\\n  Ambience is not that ...        []   \n",
       "3  [('Rated 4.0', \"RATED\\n  Great food and proper...        []   \n",
       "4  [('Rated 4.0', 'RATED\\n  Very good restaurant ...        []   \n",
       "\n",
       "  listed_in(type) listed_in(city)  \n",
       "0          Buffet    Banashankari  \n",
       "1          Buffet    Banashankari  \n",
       "2          Buffet    Banashankari  \n",
       "3          Buffet    Banashankari  \n",
       "4          Buffet    Banashankari  "
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "df = pd.read_csv('/kaggle/input/zomato-bangalore-restaurants/zomato.csv')\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:30.260902Z",
     "iopub.status.busy": "2024-09-25T09:05:30.260558Z",
     "iopub.status.idle": "2024-09-25T09:05:30.349203Z",
     "shell.execute_reply": "2024-09-25T09:05:30.348081Z",
     "shell.execute_reply.started": "2024-09-25T09:05:30.260866Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "url                                0\n",
       "address                            0\n",
       "name                               0\n",
       "online_order                       0\n",
       "book_table                         0\n",
       "rate                            7775\n",
       "votes                              0\n",
       "phone                           1208\n",
       "location                          21\n",
       "rest_type                        227\n",
       "dish_liked                     28078\n",
       "cuisines                          45\n",
       "approx_cost(for two people)      346\n",
       "reviews_list                       0\n",
       "menu_item                          0\n",
       "listed_in(type)                    0\n",
       "listed_in(city)                    0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.isna().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:30.352548Z",
     "iopub.status.busy": "2024-09-25T09:05:30.352106Z",
     "iopub.status.idle": "2024-09-25T09:05:32.154410Z",
     "shell.execute_reply": "2024-09-25T09:05:32.153434Z",
     "shell.execute_reply.started": "2024-09-25T09:05:30.352499Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.duplicated().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.156420Z",
     "iopub.status.busy": "2024-09-25T09:05:32.156024Z",
     "iopub.status.idle": "2024-09-25T09:05:32.179702Z",
     "shell.execute_reply": "2024-09-25T09:05:32.178777Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.156377Z"
    }
   },
   "outputs": [],
   "source": [
    "df = df.dropna(subset=['rate'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.181044Z",
     "iopub.status.busy": "2024-09-25T09:05:32.180743Z",
     "iopub.status.idle": "2024-09-25T09:05:32.190793Z",
     "shell.execute_reply": "2024-09-25T09:05:32.189803Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.181014Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['4.1/5', '3.8/5', '3.7/5', '3.6/5', '4.6/5', '4.0/5', '4.2/5',\n",
       "       '3.9/5', '3.1/5', '3.0/5', '3.2/5', '3.3/5', '2.8/5', '4.4/5',\n",
       "       '4.3/5', 'NEW', '2.9/5', '3.5/5', '2.6/5', '3.8 /5', '3.4/5',\n",
       "       '4.5/5', '2.5/5', '2.7/5', '4.7/5', '2.4/5', '2.2/5', '2.3/5',\n",
       "       '3.4 /5', '-', '3.6 /5', '4.8/5', '3.9 /5', '4.2 /5', '4.0 /5',\n",
       "       '4.1 /5', '3.7 /5', '3.1 /5', '2.9 /5', '3.3 /5', '2.8 /5',\n",
       "       '3.5 /5', '2.7 /5', '2.5 /5', '3.2 /5', '2.6 /5', '4.5 /5',\n",
       "       '4.3 /5', '4.4 /5', '4.9/5', '2.1/5', '2.0/5', '1.8/5', '4.6 /5',\n",
       "       '4.9 /5', '3.0 /5', '4.8 /5', '2.3 /5', '4.7 /5', '2.4 /5',\n",
       "       '2.1 /5', '2.2 /5', '2.0 /5', '1.8 /5'], dtype=object)"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['rate'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.192111Z",
     "iopub.status.busy": "2024-09-25T09:05:32.191826Z",
     "iopub.status.idle": "2024-09-25T09:05:32.241454Z",
     "shell.execute_reply": "2024-09-25T09:05:32.240768Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.192081Z"
    }
   },
   "outputs": [],
   "source": [
    "df['rate'] = df['rate'].str.replace('/5', '').replace('NEW', float('nan')).replace('-', float('nan')).astype(float)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.242769Z",
     "iopub.status.busy": "2024-09-25T09:05:32.242489Z",
     "iopub.status.idle": "2024-09-25T09:05:32.249966Z",
     "shell.execute_reply": "2024-09-25T09:05:32.248856Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.242739Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([4.1, 3.8, 3.7, 3.6, 4.6, 4. , 4.2, 3.9, 3.1, 3. , 3.2, 3.3, 2.8,\n",
       "       4.4, 4.3, nan, 2.9, 3.5, 2.6, 3.4, 4.5, 2.5, 2.7, 4.7, 2.4, 2.2,\n",
       "       2.3, 4.8, 4.9, 2.1, 2. , 1.8])"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['rate'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.254423Z",
     "iopub.status.busy": "2024-09-25T09:05:32.254081Z",
     "iopub.status.idle": "2024-09-25T09:05:32.273596Z",
     "shell.execute_reply": "2024-09-25T09:05:32.272783Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.254391Z"
    }
   },
   "outputs": [],
   "source": [
    "df = df.dropna(subset=['rate'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.274836Z",
     "iopub.status.busy": "2024-09-25T09:05:32.274558Z",
     "iopub.status.idle": "2024-09-25T09:05:32.309959Z",
     "shell.execute_reply": "2024-09-25T09:05:32.308962Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.274794Z"
    }
   },
   "outputs": [],
   "source": [
    "df['is_good'] = df['rate'].apply(lambda x: 1 if x > 3.75 else 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.311365Z",
     "iopub.status.busy": "2024-09-25T09:05:32.311094Z",
     "iopub.status.idle": "2024-09-25T09:05:32.329640Z",
     "shell.execute_reply": "2024-09-25T09:05:32.328711Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.311335Z"
    }
   },
   "outputs": [],
   "source": [
    "df = df.drop('rate', axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.331027Z",
     "iopub.status.busy": "2024-09-25T09:05:32.330719Z",
     "iopub.status.idle": "2024-09-25T09:05:32.353808Z",
     "shell.execute_reply": "2024-09-25T09:05:32.352839Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.330996Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>url</th>\n",
       "      <th>address</th>\n",
       "      <th>name</th>\n",
       "      <th>online_order</th>\n",
       "      <th>book_table</th>\n",
       "      <th>votes</th>\n",
       "      <th>phone</th>\n",
       "      <th>location</th>\n",
       "      <th>rest_type</th>\n",
       "      <th>dish_liked</th>\n",
       "      <th>cuisines</th>\n",
       "      <th>approx_cost(for two people)</th>\n",
       "      <th>reviews_list</th>\n",
       "      <th>menu_item</th>\n",
       "      <th>listed_in(type)</th>\n",
       "      <th>listed_in(city)</th>\n",
       "      <th>is_good</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>https://www.zomato.com/bangalore/jalsa-banasha...</td>\n",
       "      <td>942, 21st Main Road, 2nd Stage, Banashankari, ...</td>\n",
       "      <td>Jalsa</td>\n",
       "      <td>Yes</td>\n",
       "      <td>Yes</td>\n",
       "      <td>775</td>\n",
       "      <td>080 42297555\\r\\n+91 9743772233</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Casual Dining</td>\n",
       "      <td>Pasta, Lunch Buffet, Masala Papad, Paneer Laja...</td>\n",
       "      <td>North Indian, Mughlai, Chinese</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  A beautiful place to ...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>https://www.zomato.com/bangalore/spice-elephan...</td>\n",
       "      <td>2nd Floor, 80 Feet Road, Near Big Bazaar, 6th ...</td>\n",
       "      <td>Spice Elephant</td>\n",
       "      <td>Yes</td>\n",
       "      <td>No</td>\n",
       "      <td>787</td>\n",
       "      <td>080 41714161</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Casual Dining</td>\n",
       "      <td>Momos, Lunch Buffet, Chocolate Nirvana, Thai G...</td>\n",
       "      <td>Chinese, North Indian, Thai</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  Had been here for din...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>https://www.zomato.com/SanchurroBangalore?cont...</td>\n",
       "      <td>1112, Next to KIMS Medical College, 17th Cross...</td>\n",
       "      <td>San Churro Cafe</td>\n",
       "      <td>Yes</td>\n",
       "      <td>No</td>\n",
       "      <td>918</td>\n",
       "      <td>+91 9663487993</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Cafe, Casual Dining</td>\n",
       "      <td>Churros, Cannelloni, Minestrone Soup, Hot Choc...</td>\n",
       "      <td>Cafe, Mexican, Italian</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 3.0', \"RATED\\n  Ambience is not that ...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>https://www.zomato.com/bangalore/addhuri-udupi...</td>\n",
       "      <td>1st Floor, Annakuteera, 3rd Stage, Banashankar...</td>\n",
       "      <td>Addhuri Udupi Bhojana</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>88</td>\n",
       "      <td>+91 9620009302</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>Quick Bites</td>\n",
       "      <td>Masala Dosa</td>\n",
       "      <td>South Indian, North Indian</td>\n",
       "      <td>300</td>\n",
       "      <td>[('Rated 4.0', \"RATED\\n  Great food and proper...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>https://www.zomato.com/bangalore/grand-village...</td>\n",
       "      <td>10, 3rd Floor, Lakshmi Associates, Gandhi Baza...</td>\n",
       "      <td>Grand Village</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>166</td>\n",
       "      <td>+91 8026612447\\r\\n+91 9901210005</td>\n",
       "      <td>Basavanagudi</td>\n",
       "      <td>Casual Dining</td>\n",
       "      <td>Panipuri, Gol Gappe</td>\n",
       "      <td>North Indian, Rajasthani</td>\n",
       "      <td>600</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  Very good restaurant ...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>Banashankari</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>51709</th>\n",
       "      <td>https://www.zomato.com/bangalore/the-farm-hous...</td>\n",
       "      <td>136, SAP Labs India, KIADB Export Promotion In...</td>\n",
       "      <td>The Farm House Bar n Grill</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>34</td>\n",
       "      <td>+91 9980121279\\n+91 9900240646</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>Casual Dining, Bar</td>\n",
       "      <td>NaN</td>\n",
       "      <td>North Indian, Continental</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  Ambience- Big and spa...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Pubs and bars</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>51711</th>\n",
       "      <td>https://www.zomato.com/bangalore/bhagini-2-whi...</td>\n",
       "      <td>139/C1, Next To GR Tech Park, Pattandur Agraha...</td>\n",
       "      <td>Bhagini</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>81</td>\n",
       "      <td>080 65951222</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>Casual Dining, Bar</td>\n",
       "      <td>Biryani, Andhra Meal</td>\n",
       "      <td>Andhra, South Indian, Chinese, North Indian</td>\n",
       "      <td>800</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  A fine place to chill...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Pubs and bars</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>51712</th>\n",
       "      <td>https://www.zomato.com/bangalore/best-brews-fo...</td>\n",
       "      <td>Four Points by Sheraton Bengaluru, 43/3, White...</td>\n",
       "      <td>Best Brews - Four Points by Sheraton Bengaluru...</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>27</td>\n",
       "      <td>080 40301477</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>Bar</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Continental</td>\n",
       "      <td>1,500</td>\n",
       "      <td>[('Rated 5.0', \"RATED\\n  Food and service are ...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Pubs and bars</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>51715</th>\n",
       "      <td>https://www.zomato.com/bangalore/chime-sherato...</td>\n",
       "      <td>Sheraton Grand Bengaluru Whitefield Hotel &amp; Co...</td>\n",
       "      <td>Chime - Sheraton Grand Bengaluru Whitefield Ho...</td>\n",
       "      <td>No</td>\n",
       "      <td>Yes</td>\n",
       "      <td>236</td>\n",
       "      <td>080 49652769</td>\n",
       "      <td>ITPL Main Road, Whitefield</td>\n",
       "      <td>Bar</td>\n",
       "      <td>Cocktails, Pizza, Buttermilk</td>\n",
       "      <td>Finger Food</td>\n",
       "      <td>2,500</td>\n",
       "      <td>[('Rated 4.0', 'RATED\\n  Nice and friendly pla...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Pubs and bars</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>51716</th>\n",
       "      <td>https://www.zomato.com/bangalore/the-nest-the-...</td>\n",
       "      <td>ITPL Main Road, KIADB Export Promotion Industr...</td>\n",
       "      <td>The Nest - The Den Bengaluru</td>\n",
       "      <td>No</td>\n",
       "      <td>No</td>\n",
       "      <td>13</td>\n",
       "      <td>+91 8071117272</td>\n",
       "      <td>ITPL Main Road, Whitefield</td>\n",
       "      <td>Bar, Casual Dining</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Finger Food, North Indian, Continental</td>\n",
       "      <td>1,500</td>\n",
       "      <td>[('Rated 5.0', 'RATED\\n  Great ambience , look...</td>\n",
       "      <td>[]</td>\n",
       "      <td>Pubs and bars</td>\n",
       "      <td>Whitefield</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>41665 rows × 17 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                     url  \\\n",
       "0      https://www.zomato.com/bangalore/jalsa-banasha...   \n",
       "1      https://www.zomato.com/bangalore/spice-elephan...   \n",
       "2      https://www.zomato.com/SanchurroBangalore?cont...   \n",
       "3      https://www.zomato.com/bangalore/addhuri-udupi...   \n",
       "4      https://www.zomato.com/bangalore/grand-village...   \n",
       "...                                                  ...   \n",
       "51709  https://www.zomato.com/bangalore/the-farm-hous...   \n",
       "51711  https://www.zomato.com/bangalore/bhagini-2-whi...   \n",
       "51712  https://www.zomato.com/bangalore/best-brews-fo...   \n",
       "51715  https://www.zomato.com/bangalore/chime-sherato...   \n",
       "51716  https://www.zomato.com/bangalore/the-nest-the-...   \n",
       "\n",
       "                                                 address  \\\n",
       "0      942, 21st Main Road, 2nd Stage, Banashankari, ...   \n",
       "1      2nd Floor, 80 Feet Road, Near Big Bazaar, 6th ...   \n",
       "2      1112, Next to KIMS Medical College, 17th Cross...   \n",
       "3      1st Floor, Annakuteera, 3rd Stage, Banashankar...   \n",
       "4      10, 3rd Floor, Lakshmi Associates, Gandhi Baza...   \n",
       "...                                                  ...   \n",
       "51709  136, SAP Labs India, KIADB Export Promotion In...   \n",
       "51711  139/C1, Next To GR Tech Park, Pattandur Agraha...   \n",
       "51712  Four Points by Sheraton Bengaluru, 43/3, White...   \n",
       "51715  Sheraton Grand Bengaluru Whitefield Hotel & Co...   \n",
       "51716  ITPL Main Road, KIADB Export Promotion Industr...   \n",
       "\n",
       "                                                    name online_order  \\\n",
       "0                                                  Jalsa          Yes   \n",
       "1                                         Spice Elephant          Yes   \n",
       "2                                        San Churro Cafe          Yes   \n",
       "3                                  Addhuri Udupi Bhojana           No   \n",
       "4                                          Grand Village           No   \n",
       "...                                                  ...          ...   \n",
       "51709                         The Farm House Bar n Grill           No   \n",
       "51711                                            Bhagini           No   \n",
       "51712  Best Brews - Four Points by Sheraton Bengaluru...           No   \n",
       "51715  Chime - Sheraton Grand Bengaluru Whitefield Ho...           No   \n",
       "51716                       The Nest - The Den Bengaluru           No   \n",
       "\n",
       "      book_table  votes                             phone  \\\n",
       "0            Yes    775    080 42297555\\r\\n+91 9743772233   \n",
       "1             No    787                      080 41714161   \n",
       "2             No    918                    +91 9663487993   \n",
       "3             No     88                    +91 9620009302   \n",
       "4             No    166  +91 8026612447\\r\\n+91 9901210005   \n",
       "...          ...    ...                               ...   \n",
       "51709         No     34    +91 9980121279\\n+91 9900240646   \n",
       "51711         No     81                      080 65951222   \n",
       "51712         No     27                      080 40301477   \n",
       "51715        Yes    236                      080 49652769   \n",
       "51716         No     13                    +91 8071117272   \n",
       "\n",
       "                         location            rest_type  \\\n",
       "0                    Banashankari        Casual Dining   \n",
       "1                    Banashankari        Casual Dining   \n",
       "2                    Banashankari  Cafe, Casual Dining   \n",
       "3                    Banashankari          Quick Bites   \n",
       "4                    Basavanagudi        Casual Dining   \n",
       "...                           ...                  ...   \n",
       "51709                  Whitefield   Casual Dining, Bar   \n",
       "51711                  Whitefield   Casual Dining, Bar   \n",
       "51712                  Whitefield                  Bar   \n",
       "51715  ITPL Main Road, Whitefield                  Bar   \n",
       "51716  ITPL Main Road, Whitefield   Bar, Casual Dining   \n",
       "\n",
       "                                              dish_liked  \\\n",
       "0      Pasta, Lunch Buffet, Masala Papad, Paneer Laja...   \n",
       "1      Momos, Lunch Buffet, Chocolate Nirvana, Thai G...   \n",
       "2      Churros, Cannelloni, Minestrone Soup, Hot Choc...   \n",
       "3                                            Masala Dosa   \n",
       "4                                    Panipuri, Gol Gappe   \n",
       "...                                                  ...   \n",
       "51709                                                NaN   \n",
       "51711                               Biryani, Andhra Meal   \n",
       "51712                                                NaN   \n",
       "51715                       Cocktails, Pizza, Buttermilk   \n",
       "51716                                                NaN   \n",
       "\n",
       "                                          cuisines  \\\n",
       "0                   North Indian, Mughlai, Chinese   \n",
       "1                      Chinese, North Indian, Thai   \n",
       "2                           Cafe, Mexican, Italian   \n",
       "3                       South Indian, North Indian   \n",
       "4                         North Indian, Rajasthani   \n",
       "...                                            ...   \n",
       "51709                    North Indian, Continental   \n",
       "51711  Andhra, South Indian, Chinese, North Indian   \n",
       "51712                                  Continental   \n",
       "51715                                  Finger Food   \n",
       "51716       Finger Food, North Indian, Continental   \n",
       "\n",
       "      approx_cost(for two people)  \\\n",
       "0                             800   \n",
       "1                             800   \n",
       "2                             800   \n",
       "3                             300   \n",
       "4                             600   \n",
       "...                           ...   \n",
       "51709                         800   \n",
       "51711                         800   \n",
       "51712                       1,500   \n",
       "51715                       2,500   \n",
       "51716                       1,500   \n",
       "\n",
       "                                            reviews_list menu_item  \\\n",
       "0      [('Rated 4.0', 'RATED\\n  A beautiful place to ...        []   \n",
       "1      [('Rated 4.0', 'RATED\\n  Had been here for din...        []   \n",
       "2      [('Rated 3.0', \"RATED\\n  Ambience is not that ...        []   \n",
       "3      [('Rated 4.0', \"RATED\\n  Great food and proper...        []   \n",
       "4      [('Rated 4.0', 'RATED\\n  Very good restaurant ...        []   \n",
       "...                                                  ...       ...   \n",
       "51709  [('Rated 4.0', 'RATED\\n  Ambience- Big and spa...        []   \n",
       "51711  [('Rated 4.0', 'RATED\\n  A fine place to chill...        []   \n",
       "51712  [('Rated 5.0', \"RATED\\n  Food and service are ...        []   \n",
       "51715  [('Rated 4.0', 'RATED\\n  Nice and friendly pla...        []   \n",
       "51716  [('Rated 5.0', 'RATED\\n  Great ambience , look...        []   \n",
       "\n",
       "      listed_in(type) listed_in(city)  is_good  \n",
       "0              Buffet    Banashankari        1  \n",
       "1              Buffet    Banashankari        1  \n",
       "2              Buffet    Banashankari        1  \n",
       "3              Buffet    Banashankari        0  \n",
       "4              Buffet    Banashankari        1  \n",
       "...               ...             ...      ...  \n",
       "51709   Pubs and bars      Whitefield        0  \n",
       "51711   Pubs and bars      Whitefield        0  \n",
       "51712   Pubs and bars      Whitefield        0  \n",
       "51715   Pubs and bars      Whitefield        1  \n",
       "51716   Pubs and bars      Whitefield        0  \n",
       "\n",
       "[41665 rows x 17 columns]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.355315Z",
     "iopub.status.busy": "2024-09-25T09:05:32.354978Z",
     "iopub.status.idle": "2024-09-25T09:05:32.371847Z",
     "shell.execute_reply": "2024-09-25T09:05:32.370699Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.355284Z"
    }
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/tmp/ipykernel_609/3962288892.py:1: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.\n",
      "The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.\n",
      "\n",
      "For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.\n",
      "\n",
      "\n",
      "  df['dish_liked'].fillna(df['dish_liked'].mode()[0], inplace=True)\n"
     ]
    }
   ],
   "source": [
    "df['dish_liked'].fillna(df['dish_liked'].mode()[0], inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.373226Z",
     "iopub.status.busy": "2024-09-25T09:05:32.372948Z",
     "iopub.status.idle": "2024-09-25T09:05:32.405589Z",
     "shell.execute_reply": "2024-09-25T09:05:32.404649Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.373196Z"
    }
   },
   "outputs": [],
   "source": [
    "df = df.dropna(subset=['rest_type', 'cuisines', 'approx_cost(for two people)'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.407349Z",
     "iopub.status.busy": "2024-09-25T09:05:32.407040Z",
     "iopub.status.idle": "2024-09-25T09:05:32.474907Z",
     "shell.execute_reply": "2024-09-25T09:05:32.473973Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.407316Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "url                              0\n",
       "address                          0\n",
       "name                             0\n",
       "online_order                     0\n",
       "book_table                       0\n",
       "votes                            0\n",
       "phone                          576\n",
       "location                         0\n",
       "rest_type                        0\n",
       "dish_liked                       0\n",
       "cuisines                         0\n",
       "approx_cost(for two people)      0\n",
       "reviews_list                     0\n",
       "menu_item                        0\n",
       "listed_in(type)                  0\n",
       "listed_in(city)                  0\n",
       "is_good                          0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.isna().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.477266Z",
     "iopub.status.busy": "2024-09-25T09:05:32.475919Z",
     "iopub.status.idle": "2024-09-25T09:05:32.536881Z",
     "shell.execute_reply": "2024-09-25T09:05:32.536062Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.477233Z"
    }
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/tmp/ipykernel_609/3214176263.py:2: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  df['approx_cost(for two people)'] = df['approx_cost(for two people)'].str.replace(',', '')\n",
      "/tmp/ipykernel_609/3214176263.py:5: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'])\n"
     ]
    }
   ],
   "source": [
    "# Remove the commas from the approx_cost column\n",
    "df['approx_cost(for two people)'] = df['approx_cost(for two people)'].str.replace(',', '')\n",
    "\n",
    "# Convert the approx_cost column to a numerical type\n",
    "df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.538588Z",
     "iopub.status.busy": "2024-09-25T09:05:32.538221Z",
     "iopub.status.idle": "2024-09-25T09:05:32.616900Z",
     "shell.execute_reply": "2024-09-25T09:05:32.615725Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.538555Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Index: 41263 entries, 0 to 51716\n",
      "Data columns (total 17 columns):\n",
      " #   Column                       Non-Null Count  Dtype \n",
      "---  ------                       --------------  ----- \n",
      " 0   url                          41263 non-null  object\n",
      " 1   address                      41263 non-null  object\n",
      " 2   name                         41263 non-null  object\n",
      " 3   online_order                 41263 non-null  object\n",
      " 4   book_table                   41263 non-null  object\n",
      " 5   votes                        41263 non-null  int64 \n",
      " 6   phone                        40687 non-null  object\n",
      " 7   location                     41263 non-null  object\n",
      " 8   rest_type                    41263 non-null  object\n",
      " 9   dish_liked                   41263 non-null  object\n",
      " 10  cuisines                     41263 non-null  object\n",
      " 11  approx_cost(for two people)  41263 non-null  int64 \n",
      " 12  reviews_list                 41263 non-null  object\n",
      " 13  menu_item                    41263 non-null  object\n",
      " 14  listed_in(type)              41263 non-null  object\n",
      " 15  listed_in(city)              41263 non-null  object\n",
      " 16  is_good                      41263 non-null  int64 \n",
      "dtypes: int64(3), object(14)\n",
      "memory usage: 5.7+ MB\n"
     ]
    }
   ],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.618307Z",
     "iopub.status.busy": "2024-09-25T09:05:32.618004Z",
     "iopub.status.idle": "2024-09-25T09:05:32.641594Z",
     "shell.execute_reply": "2024-09-25T09:05:32.640742Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.618274Z"
    }
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/tmp/ipykernel_609/3441621149.py:1: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  df.drop(df[df['votes'] < 100].index, inplace=True)\n"
     ]
    }
   ],
   "source": [
    "df.drop(df[df['votes'] < 100].index, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.643122Z",
     "iopub.status.busy": "2024-09-25T09:05:32.642711Z",
     "iopub.status.idle": "2024-09-25T09:05:32.650392Z",
     "shell.execute_reply": "2024-09-25T09:05:32.649343Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.643088Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0        [('Rated 4.0', 'RATED\\n  A beautiful place to ...\n",
       "1        [('Rated 4.0', 'RATED\\n  Had been here for din...\n",
       "2        [('Rated 3.0', \"RATED\\n  Ambience is not that ...\n",
       "4        [('Rated 4.0', 'RATED\\n  Very good restaurant ...\n",
       "5        [('Rated 3.0', 'RATED\\n  Food 3/5\\nAmbience 3/...\n",
       "                               ...                        \n",
       "51703    [('Rated 4.0', \"RATED\\n  I had :-\\n\\n1. Italia...\n",
       "51704    [('Rated 3.0', 'RATED\\n  Like this place for z...\n",
       "51705    [('Rated 3.0', \"RATED\\n  Nice place to hangout...\n",
       "51708    [('Rated 3.0', 'RATED\\n  Place is good not tha...\n",
       "51715    [('Rated 4.0', 'RATED\\n  Nice and friendly pla...\n",
       "Name: reviews_list, Length: 18245, dtype: object"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.reviews_list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.651840Z",
     "iopub.status.busy": "2024-09-25T09:05:32.651528Z",
     "iopub.status.idle": "2024-09-25T09:05:32.670622Z",
     "shell.execute_reply": "2024-09-25T09:05:32.669772Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.651784Z"
    }
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/tmp/ipykernel_609/1653960700.py:6: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  df['online_order_encoded'] = le.fit_transform(df['online_order'])\n",
      "/tmp/ipykernel_609/1653960700.py:7: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  df['book_table_encoded'] = le.fit_transform(df['book_table'])\n"
     ]
    }
   ],
   "source": [
    "from sklearn.preprocessing import LabelEncoder\n",
    "\n",
    "\n",
    "# Create a LabelEncoder to encode the categorical feature\n",
    "le = LabelEncoder()\n",
    "df['online_order_encoded'] = le.fit_transform(df['online_order'])\n",
    "df['book_table_encoded'] = le.fit_transform(df['book_table'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.672633Z",
     "iopub.status.busy": "2024-09-25T09:05:32.671885Z",
     "iopub.status.idle": "2024-09-25T09:05:32.682755Z",
     "shell.execute_reply": "2024-09-25T09:05:32.681978Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.672590Z"
    }
   },
   "outputs": [],
   "source": [
    "df = df.drop(columns=['online_order', 'book_table','url','name','address','phone'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.684222Z",
     "iopub.status.busy": "2024-09-25T09:05:32.683920Z",
     "iopub.status.idle": "2024-09-25T09:05:32.709761Z",
     "shell.execute_reply": "2024-09-25T09:05:32.708806Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.684190Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Index: 18245 entries, 0 to 51715\n",
      "Data columns (total 13 columns):\n",
      " #   Column                       Non-Null Count  Dtype \n",
      "---  ------                       --------------  ----- \n",
      " 0   votes                        18245 non-null  int64 \n",
      " 1   location                     18245 non-null  object\n",
      " 2   rest_type                    18245 non-null  object\n",
      " 3   dish_liked                   18245 non-null  object\n",
      " 4   cuisines                     18245 non-null  object\n",
      " 5   approx_cost(for two people)  18245 non-null  int64 \n",
      " 6   reviews_list                 18245 non-null  object\n",
      " 7   menu_item                    18245 non-null  object\n",
      " 8   listed_in(type)              18245 non-null  object\n",
      " 9   listed_in(city)              18245 non-null  object\n",
      " 10  is_good                      18245 non-null  int64 \n",
      " 11  online_order_encoded         18245 non-null  int64 \n",
      " 12  book_table_encoded           18245 non-null  int64 \n",
      "dtypes: int64(5), object(8)\n",
      "memory usage: 1.9+ MB\n"
     ]
    }
   ],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.711260Z",
     "iopub.status.busy": "2024-09-25T09:05:32.710950Z",
     "iopub.status.idle": "2024-09-25T09:05:32.733229Z",
     "shell.execute_reply": "2024-09-25T09:05:32.732244Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.711228Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "votes                          0\n",
       "location                       0\n",
       "rest_type                      0\n",
       "dish_liked                     0\n",
       "cuisines                       0\n",
       "approx_cost(for two people)    0\n",
       "reviews_list                   0\n",
       "menu_item                      0\n",
       "listed_in(type)                0\n",
       "listed_in(city)                0\n",
       "is_good                        0\n",
       "online_order_encoded           0\n",
       "book_table_encoded             0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.isna().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.737853Z",
     "iopub.status.busy": "2024-09-25T09:05:32.737429Z",
     "iopub.status.idle": "2024-09-25T09:05:32.744667Z",
     "shell.execute_reply": "2024-09-25T09:05:32.743881Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.737794Z"
    }
   },
   "outputs": [],
   "source": [
    "X = df.drop(columns=['is_good'])  # features\n",
    "y = df['is_good']  # target variable"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.745973Z",
     "iopub.status.busy": "2024-09-25T09:05:32.745655Z",
     "iopub.status.idle": "2024-09-25T09:05:32.752711Z",
     "shell.execute_reply": "2024-09-25T09:05:32.751833Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.745943Z"
    }
   },
   "outputs": [],
   "source": [
    "numeric_cols = ['votes', 'approx_cost(for two people)', 'online_order_encoded', 'book_table_encoded']\n",
    "categorical_cols = ['location', 'rest_type', 'dish_liked', 'cuisines', 'reviews_list', 'menu_item', 'listed_in(type)', 'listed_in(city)']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "execution": {
     "iopub.status.busy": "2024-09-25T10:26:14.904260Z",
     "iopub.status.idle": "2024-09-25T10:26:14.904751Z",
     "shell.execute_reply": "2024-09-25T10:26:14.904526Z",
     "shell.execute_reply.started": "2024-09-25T10:26:14.904495Z"
    }
   },
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "pd.plotting.scatter_matrix(X, alpha=0.7, figsize=(10, 10), diagonal='kde')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:32.754679Z",
     "iopub.status.busy": "2024-09-25T09:05:32.754089Z",
     "iopub.status.idle": "2024-09-25T09:05:33.026837Z",
     "shell.execute_reply": "2024-09-25T09:05:33.026013Z",
     "shell.execute_reply.started": "2024-09-25T09:05:32.754644Z"
    }
   },
   "outputs": [],
   "source": [
    "from sklearn.model_selection import cross_validate\n",
    "from sklearn.model_selection import *\n",
    "from sklearn.impute import SimpleImputer\n",
    "from sklearn.base import BaseEstimator, TransformerMixin\n",
    "\n",
    "class MostFrequentImputer(BaseEstimator, TransformerMixin):\n",
    "    def fit(self, X, y=None):\n",
    "        self.most_frequent_ = X.mode().iloc[0]\n",
    "        return self\n",
    "\n",
    "    def transform(self, X):\n",
    "        return X.fillna(self.most_frequent_)\n",
    "\n",
    "imputer = MostFrequentImputer()\n",
    "X_imputed = imputer.fit_transform(X)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:33.028214Z",
     "iopub.status.busy": "2024-09-25T09:05:33.027914Z",
     "iopub.status.idle": "2024-09-25T09:05:33.035086Z",
     "shell.execute_reply": "2024-09-25T09:05:33.034152Z",
     "shell.execute_reply.started": "2024-09-25T09:05:33.028183Z"
    }
   },
   "outputs": [],
   "source": [
    "# Separate the columns explicitly\n",
    "numeric_columns = ['votes', 'approx_cost(for two people)', 'online_order_encoded', 'book_table_encoded']\n",
    "categorical_columns = ['location', 'rest_type', 'dish_liked', 'cuisines', 'reviews_list', 'menu_item', 'listed_in(type)', 'listed_in(city)']\n",
    "\n",
    "# Define your preprocessor\n",
    "preprocessor = ColumnTransformer(\n",
    "    transformers=[\n",
    "        ('num', Pipeline(steps=[\n",
    "            ('imputer', SimpleImputer(strategy='mean')),  # or 'median'\n",
    "            ('scaler', StandardScaler())]), numeric_columns),\n",
    "        \n",
    "        ('cat', Pipeline(steps=[\n",
    "            ('imputer', SimpleImputer(strategy='most_frequent')),\n",
    "            ('encoder', OneHotEncoder(handle_unknown='ignore'))]), categorical_columns)\n",
    "    ])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:05:33.038142Z",
     "iopub.status.busy": "2024-09-25T09:05:33.037416Z",
     "iopub.status.idle": "2024-09-25T09:06:06.675496Z",
     "shell.execute_reply": "2024-09-25T09:06:06.674440Z",
     "shell.execute_reply.started": "2024-09-25T09:05:33.038098Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'fit_time': array([5.12887931, 6.48927188, 7.60115457, 8.28826046, 5.42897463]), 'score_time': array([0.14728069, 0.11554837, 0.14819741, 0.11404538, 0.14772725]), 'test_score': array([0.91614141, 0.85722116, 0.82433543, 0.92162236, 0.9229926 ])}\n"
     ]
    }
   ],
   "source": [
    "pipeline = Pipeline(steps=[\n",
    "    ('preprocessor', preprocessor),\n",
    "    ('model', LogisticRegression(max_iter=1000, multi_class='ovr'))  # You can change this to RandomForestClassifier or other models\n",
    "])\n",
    "\n",
    "# Perform cross-validation\n",
    "cv_results1 = cross_validate(pipeline, X, y, scoring='accuracy')\n",
    "\n",
    "# Print cross-validation results\n",
    "print(cv_results1)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:06:06.678436Z",
     "iopub.status.busy": "2024-09-25T09:06:06.677736Z",
     "iopub.status.idle": "2024-09-25T09:06:35.646878Z",
     "shell.execute_reply": "2024-09-25T09:06:35.645955Z",
     "shell.execute_reply.started": "2024-09-25T09:06:06.678384Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'fit_time': array([5.27141595, 6.89742732, 6.04638386, 4.86807919, 5.18713093]), 'score_time': array([0.1312027 , 0.1499877 , 0.15149331, 0.12728429, 0.10764003]), 'test_score': array([0.91614141, 0.85722116, 0.82433543, 0.92162236, 0.9229926 ])}\n"
     ]
    }
   ],
   "source": [
    "\n",
    "\n",
    "# For numeric columns, use SimpleImputer with mean strategy, followed by scaling\n",
    "numeric_transformer = Pipeline(steps=[\n",
    "    ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with the mean\n",
    "    ('scaler', StandardScaler())  # Scale the numeric features\n",
    "])\n",
    "\n",
    "# For categorical columns, use SimpleImputer with most_frequent strategy, followed by one-hot encoding\n",
    "categorical_transformer = Pipeline(steps=[\n",
    "    ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing values with most frequent value\n",
    "    ('encoder', OneHotEncoder(handle_unknown='ignore'))  # One-hot encode the categorical features\n",
    "])\n",
    "\n",
    "# Create a ColumnTransformer to handle the entire dataset\n",
    "preprocessor = ColumnTransformer(\n",
    "    transformers=[\n",
    "        ('num', numeric_transformer, numeric_cols),  # Apply numeric transformation to numeric columns\n",
    "        ('cat', categorical_transformer, categorical_cols)  # Apply categorical transformation to categorical columns\n",
    "    ]\n",
    ")\n",
    "\n",
    "# Create a pipeline that includes the preprocessor and a model (e.g., LogisticRegression or RandomForestClassifier)\n",
    "pipeline = Pipeline(steps=[\n",
    "    ('preprocessor', preprocessor),\n",
    "    ('model', LogisticRegression(max_iter=1000, multi_class='ovr'))  # You can change this to RandomForestClassifier or other models\n",
    "])\n",
    "\n",
    "# Perform cross-validation\n",
    "cv_results1 = cross_validate(pipeline, X, y, scoring='accuracy')\n",
    "\n",
    "# Print cross-validation results\n",
    "print(cv_results1)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:06:35.651415Z",
     "iopub.status.busy": "2024-09-25T09:06:35.650873Z",
     "iopub.status.idle": "2024-09-25T09:06:35.656791Z",
     "shell.execute_reply": "2024-09-25T09:06:35.655998Z",
     "shell.execute_reply.started": "2024-09-25T09:06:35.651373Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Average accuracy: 0.89\n"
     ]
    }
   ],
   "source": [
    "average_accuracy1 = cv_results1['test_score'].mean()\n",
    "print(f'Average accuracy: {average_accuracy1:.2f}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:06:35.659951Z",
     "iopub.status.busy": "2024-09-25T09:06:35.659094Z",
     "iopub.status.idle": "2024-09-25T09:07:42.437352Z",
     "shell.execute_reply": "2024-09-25T09:07:42.436290Z",
     "shell.execute_reply.started": "2024-09-25T09:06:35.659905Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'fit_time': array([13.21192551, 13.19071817, 13.02320957, 13.43034053, 12.56810284]), 'score_time': array([0.26315331, 0.262393  , 0.26963663, 0.26233959, 0.26634216]), 'test_score': array([0.86763497, 0.87832283, 0.84269663, 0.93943546, 0.91751165])}\n"
     ]
    }
   ],
   "source": [
    "classifier_pipeline2 = Pipeline(steps=[\n",
    "    ('preprocessor', preprocessor),\n",
    "    ('model', RandomForestClassifier(n_estimators=100))\n",
    "])\n",
    "\n",
    "# Perform cross-validation\n",
    "cv_results2 = cross_validate(classifier_pipeline2, X, y, scoring='accuracy')\n",
    "print(cv_results2)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:07:42.439033Z",
     "iopub.status.busy": "2024-09-25T09:07:42.438679Z",
     "iopub.status.idle": "2024-09-25T09:07:42.444720Z",
     "shell.execute_reply": "2024-09-25T09:07:42.443593Z",
     "shell.execute_reply.started": "2024-09-25T09:07:42.438997Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Average accuracy: 0.89\n"
     ]
    }
   ],
   "source": [
    "average_accuracy2 = cv_results2['test_score'].mean()\n",
    "print(f'Average accuracy: {average_accuracy2:.2f}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:10:51.448655Z",
     "iopub.status.busy": "2024-09-25T09:10:51.448340Z",
     "iopub.status.idle": "2024-09-25T09:11:07.146418Z",
     "shell.execute_reply": "2024-09-25T09:11:07.145468Z",
     "shell.execute_reply.started": "2024-09-25T09:10:51.448622Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'fit_time': array([0.16870618, 0.17167449, 0.16160035, 0.16615462, 0.16193485]), 'score_time': array([2.89416552, 2.87148404, 3.55144548, 2.80960274, 2.7113843 ]), 'test_score': array([0.92107427, 0.91915593, 0.9114826 , 0.94984927, 0.90463141])}\n"
     ]
    }
   ],
   "source": [
    "from sklearn.neighbors import KNeighborsClassifier\n",
    "\n",
    "# Change the model to KNeighborsClassifier\n",
    "model_KNN5 = Pipeline(steps=[\n",
    "    ('preprocessor', preprocessor),\n",
    "    ('model', KNeighborsClassifier(n_neighbors=5))  # KNN with 5 neighbors\n",
    "])\n",
    "\n",
    "# Perform cross-validation\n",
    "cv_results5 = cross_validate(model_KNN5, X, y, scoring='accuracy')\n",
    "print(cv_results5)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:11:07.147839Z",
     "iopub.status.busy": "2024-09-25T09:11:07.147521Z",
     "iopub.status.idle": "2024-09-25T09:11:07.153308Z",
     "shell.execute_reply": "2024-09-25T09:11:07.152245Z",
     "shell.execute_reply.started": "2024-09-25T09:11:07.147792Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Average accuracy: 0.92\n"
     ]
    }
   ],
   "source": [
    "average_accuracy5 = cv_results5['test_score'].mean()\n",
    "print(f'Average accuracy: {average_accuracy5:.2f}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:11:07.154711Z",
     "iopub.status.busy": "2024-09-25T09:11:07.154378Z",
     "iopub.status.idle": "2024-09-25T09:11:07.169093Z",
     "shell.execute_reply": "2024-09-25T09:11:07.168103Z",
     "shell.execute_reply.started": "2024-09-25T09:11:07.154678Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cross-validation accuracy scores:  [0.92107427 0.91915593 0.9114826  0.94984927 0.90463141]\n",
      "Standard deviation of accuracy:  0.015452596111963542\n"
     ]
    }
   ],
   "source": [
    "print(\"Cross-validation accuracy scores: \", cv_results5['test_score'])\n",
    "print(\"Standard deviation of accuracy: \", cv_results5['test_score'].std())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:11:07.170345Z",
     "iopub.status.busy": "2024-09-25T09:11:07.169987Z",
     "iopub.status.idle": "2024-09-25T09:11:14.175715Z",
     "shell.execute_reply": "2024-09-25T09:11:14.174754Z",
     "shell.execute_reply.started": "2024-09-25T09:11:07.170313Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-1 {color: black;background-color: white;}#sk-container-id-1 pre{padding: 0;}#sk-container-id-1 div.sk-toggleable {background-color: white;}#sk-container-id-1 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-1 label.sk-toggleable__label-arrow:before {content: \"▸\";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-1 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-1 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-1 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: \"▾\";}#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-1 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-1 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-1 div.sk-parallel-item::after {content: \"\";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-serial::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-1 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-1 div.sk-item {position: relative;z-index: 1;}#sk-container-id-1 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-1 div.sk-item::before, #sk-container-id-1 div.sk-parallel-item::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-1 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-1 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-1 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-1 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-1 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-1 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-1 div.sk-label-container {text-align: center;}#sk-container-id-1 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-1 div.sk-text-repr-fallback {display: none;}</style><div id=\"sk-container-id-1\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>Pipeline(steps=[(&#x27;preprocessor&#x27;,\n",
       "                 ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  (&#x27;scaler&#x27;,\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  [&#x27;votes&#x27;,\n",
       "                                                   &#x27;approx_cost(for two &#x27;\n",
       "                                                   &#x27;people)&#x27;,\n",
       "                                                   &#x27;online_order_encoded&#x27;,\n",
       "                                                   &#x27;book_table_encoded&#x27;]),\n",
       "                                                 (&#x27;cat&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                                  (&#x27;encoder&#x27;,\n",
       "                                                                   OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                                  [&#x27;location&#x27;, &#x27;rest_type&#x27;,\n",
       "                                                   &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;,\n",
       "                                                   &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                                   &#x27;listed_in(type)&#x27;,\n",
       "                                                   &#x27;listed_in(city)&#x27;])])),\n",
       "                (&#x27;model&#x27;,\n",
       "                 LogisticRegression(max_iter=1000, multi_class=&#x27;ovr&#x27;))])</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item sk-dashed-wrapped\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-1\" type=\"checkbox\" ><label for=\"sk-estimator-id-1\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">Pipeline</label><div class=\"sk-toggleable__content\"><pre>Pipeline(steps=[(&#x27;preprocessor&#x27;,\n",
       "                 ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  (&#x27;scaler&#x27;,\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  [&#x27;votes&#x27;,\n",
       "                                                   &#x27;approx_cost(for two &#x27;\n",
       "                                                   &#x27;people)&#x27;,\n",
       "                                                   &#x27;online_order_encoded&#x27;,\n",
       "                                                   &#x27;book_table_encoded&#x27;]),\n",
       "                                                 (&#x27;cat&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                                  (&#x27;encoder&#x27;,\n",
       "                                                                   OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                                  [&#x27;location&#x27;, &#x27;rest_type&#x27;,\n",
       "                                                   &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;,\n",
       "                                                   &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                                   &#x27;listed_in(type)&#x27;,\n",
       "                                                   &#x27;listed_in(city)&#x27;])])),\n",
       "                (&#x27;model&#x27;,\n",
       "                 LogisticRegression(max_iter=1000, multi_class=&#x27;ovr&#x27;))])</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item sk-dashed-wrapped\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-2\" type=\"checkbox\" ><label for=\"sk-estimator-id-2\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">preprocessor: ColumnTransformer</label><div class=\"sk-toggleable__content\"><pre>ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                 Pipeline(steps=[(&#x27;imputer&#x27;, SimpleImputer()),\n",
       "                                                 (&#x27;scaler&#x27;, StandardScaler())]),\n",
       "                                 [&#x27;votes&#x27;, &#x27;approx_cost(for two people)&#x27;,\n",
       "                                  &#x27;online_order_encoded&#x27;,\n",
       "                                  &#x27;book_table_encoded&#x27;]),\n",
       "                                (&#x27;cat&#x27;,\n",
       "                                 Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                  SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                 (&#x27;encoder&#x27;,\n",
       "                                                  OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                 [&#x27;location&#x27;, &#x27;rest_type&#x27;, &#x27;dish_liked&#x27;,\n",
       "                                  &#x27;cuisines&#x27;, &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                  &#x27;listed_in(type)&#x27;, &#x27;listed_in(city)&#x27;])])</pre></div></div></div><div class=\"sk-parallel\"><div class=\"sk-parallel-item\"><div class=\"sk-item\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-3\" type=\"checkbox\" ><label for=\"sk-estimator-id-3\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">num</label><div class=\"sk-toggleable__content\"><pre>[&#x27;votes&#x27;, &#x27;approx_cost(for two people)&#x27;, &#x27;online_order_encoded&#x27;, &#x27;book_table_encoded&#x27;]</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-4\" type=\"checkbox\" ><label for=\"sk-estimator-id-4\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">SimpleImputer</label><div class=\"sk-toggleable__content\"><pre>SimpleImputer()</pre></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-5\" type=\"checkbox\" ><label for=\"sk-estimator-id-5\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">StandardScaler</label><div class=\"sk-toggleable__content\"><pre>StandardScaler()</pre></div></div></div></div></div></div></div></div><div class=\"sk-parallel-item\"><div class=\"sk-item\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-6\" type=\"checkbox\" ><label for=\"sk-estimator-id-6\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">cat</label><div class=\"sk-toggleable__content\"><pre>[&#x27;location&#x27;, &#x27;rest_type&#x27;, &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;, &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;, &#x27;listed_in(type)&#x27;, &#x27;listed_in(city)&#x27;]</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-7\" type=\"checkbox\" ><label for=\"sk-estimator-id-7\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">SimpleImputer</label><div class=\"sk-toggleable__content\"><pre>SimpleImputer(strategy=&#x27;most_frequent&#x27;)</pre></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-8\" type=\"checkbox\" ><label for=\"sk-estimator-id-8\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">OneHotEncoder</label><div class=\"sk-toggleable__content\"><pre>OneHotEncoder(handle_unknown=&#x27;ignore&#x27;)</pre></div></div></div></div></div></div></div></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-9\" type=\"checkbox\" ><label for=\"sk-estimator-id-9\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">LogisticRegression</label><div class=\"sk-toggleable__content\"><pre>LogisticRegression(max_iter=1000, multi_class=&#x27;ovr&#x27;)</pre></div></div></div></div></div></div></div>"
      ],
      "text/plain": [
       "Pipeline(steps=[('preprocessor',\n",
       "                 ColumnTransformer(transformers=[('num',\n",
       "                                                  Pipeline(steps=[('imputer',\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  ('scaler',\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  ['votes',\n",
       "                                                   'approx_cost(for two '\n",
       "                                                   'people)',\n",
       "                                                   'online_order_encoded',\n",
       "                                                   'book_table_encoded']),\n",
       "                                                 ('cat',\n",
       "                                                  Pipeline(steps=[('imputer',\n",
       "                                                                   SimpleImputer(strategy='most_frequent')),\n",
       "                                                                  ('encoder',\n",
       "                                                                   OneHotEncoder(handle_unknown='ignore'))]),\n",
       "                                                  ['location', 'rest_type',\n",
       "                                                   'dish_liked', 'cuisines',\n",
       "                                                   'reviews_list', 'menu_item',\n",
       "                                                   'listed_in(type)',\n",
       "                                                   'listed_in(city)'])])),\n",
       "                ('model',\n",
       "                 LogisticRegression(max_iter=1000, multi_class='ovr'))])"
      ]
     },
     "execution_count": 40,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pipeline.fit(X, y)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:11:14.177319Z",
     "iopub.status.busy": "2024-09-25T09:11:14.176979Z",
     "iopub.status.idle": "2024-09-25T09:11:14.181504Z",
     "shell.execute_reply": "2024-09-25T09:11:14.180640Z",
     "shell.execute_reply.started": "2024-09-25T09:11:14.177275Z"
    }
   },
   "outputs": [],
   "source": [
    "from sklearn.model_selection import GridSearchCV\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:11:14.182861Z",
     "iopub.status.busy": "2024-09-25T09:11:14.182557Z",
     "iopub.status.idle": "2024-09-25T09:14:27.401268Z",
     "shell.execute_reply": "2024-09-25T09:14:27.400473Z",
     "shell.execute_reply.started": "2024-09-25T09:11:14.182803Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Best Parameters: {'model__C': 10, 'preprocessor__cat__imputer__strategy': 'most_frequent', 'preprocessor__num__imputer__strategy': 'mean'}\n",
      "Best Score: 0.9120306933406412\n"
     ]
    }
   ],
   "source": [
    "param_grid = {\n",
    "    'preprocessor__num__imputer__strategy': ['mean', 'median'],  # only valid for numeric columns\n",
    "    'preprocessor__cat__imputer__strategy': ['most_frequent'],  # valid for categorical columns\n",
    "    'model__C': [0.1, 1, 10]  # assuming you're using a logistic regression model\n",
    "}\n",
    "\n",
    "# Perform GridSearchCV\n",
    "grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')\n",
    "\n",
    "# Fit the grid search\n",
    "grid_search.fit(X, y)\n",
    "\n",
    "# Output the best parameters and score\n",
    "print(\"Best Parameters:\", grid_search.best_params_)\n",
    "print(\"Best Score:\", grid_search.best_score_)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:14:27.404181Z",
     "iopub.status.busy": "2024-09-25T09:14:27.402949Z",
     "iopub.status.idle": "2024-09-25T09:15:11.792377Z",
     "shell.execute_reply": "2024-09-25T09:15:11.791309Z",
     "shell.execute_reply.started": "2024-09-25T09:14:27.404141Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.9120306933406412\n"
     ]
    }
   ],
   "source": [
    "scores = cross_val_score(grid_search.best_estimator_, X, y, cv=5, scoring='accuracy')\n",
    "print(\"Accuracy:\", scores.mean())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:15:11.793799Z",
     "iopub.status.busy": "2024-09-25T09:15:11.793495Z",
     "iopub.status.idle": "2024-09-25T09:15:26.491544Z",
     "shell.execute_reply": "2024-09-25T09:15:26.490321Z",
     "shell.execute_reply.started": "2024-09-25T09:15:11.793767Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.9992874760208276\n",
      "Classification Report:\n",
      "               precision    recall  f1-score   support\n",
      "\n",
      "           0       1.00      1.00      1.00      3429\n",
      "           1       1.00      1.00      1.00     14816\n",
      "\n",
      "    accuracy                           1.00     18245\n",
      "   macro avg       1.00      1.00      1.00     18245\n",
      "weighted avg       1.00      1.00      1.00     18245\n",
      "\n",
      "Confusion Matrix:\n",
      " [[ 3422     7]\n",
      " [    6 14810]]\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "['best_pipeline_model.pkl']"
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from sklearn.model_selection import GridSearchCV, cross_val_score\n",
    "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.impute import SimpleImputer\n",
    "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.compose import ColumnTransformer\n",
    "import joblib\n",
    "\n",
    "best_pipeline = grid_search.best_estimator_\n",
    "best_pipeline.fit(X, y)\n",
    "\n",
    "# Predict on the training data (or a separate test set)\n",
    "y_pred = best_pipeline.predict(X)\n",
    "\n",
    "# Print evaluation metrics\n",
    "print(\"Accuracy:\", accuracy_score(y, y_pred))\n",
    "print(\"Classification Report:\\n\", classification_report(y, y_pred))\n",
    "print(\"Confusion Matrix:\\n\", confusion_matrix(y, y_pred))\n",
    "\n",
    "# Save the best model for future use\n",
    "joblib.dump(best_pipeline, 'best_pipeline_model.pkl')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:15:26.494427Z",
     "iopub.status.busy": "2024-09-25T09:15:26.493683Z",
     "iopub.status.idle": "2024-09-25T09:15:27.286784Z",
     "shell.execute_reply": "2024-09-25T09:15:27.285852Z",
     "shell.execute_reply.started": "2024-09-25T09:15:26.494380Z"
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAiwAAAHHCAYAAACcHAM1AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/xnp5ZAAAACXBIWXMAAA9hAAAPYQGoP6dpAABO/ElEQVR4nO3deVxUZfs/8M8AMiDKpiyOIuISQpJrIe5+JXBN0lKUEg31qcAN90wElyhMTdzIFjHTUitI0VSSFFNSRHEhJVHUTAdUBAIFgTm/P/xxagKVceY4I3zez+u8Xs593+c+15ken67nus99RiYIggAiIiIiA2ak7wCIiIiIHocJCxERERk8JixERERk8JiwEBERkcFjwkJEREQGjwkLERERGTwmLERERGTwmLAQERGRwWPCQkRERAaPCQuRhC5cuAAfHx9YWVlBJpMhPj5ep/NfvnwZMpkMsbGxOp33WdanTx/06dNH32EQkY4xYaFa7+LFi/jf//6Hli1bwszMDJaWlujevTtWrlyJe/fuSXrtwMBAnDlzBkuWLMGmTZvQpUsXSa/3NI0dOxYymQyWlpbVfo8XLlyATCaDTCbDxx9/rPH8169fR3h4ONLT03UQLRE960z0HQCRlHbt2oXXX38dcrkcY8aMQbt27XD//n38+uuvmDlzJjIyMrB+/XpJrn3v3j2kpKRg3rx5CAkJkeQazs7OuHfvHurVqyfJ/I9jYmKCu3fvYufOnRgxYoRa3+bNm2FmZoaSkpInmvv69euIiIhAixYt0KFDhxqft2/fvie6HhEZNiYsVGtlZ2fD398fzs7OSEpKQpMmTcS+4OBgZGVlYdeuXZJd/+bNmwAAa2trya4hk8lgZmYm2fyPI5fL0b17d3zzzTdVEpYtW7Zg0KBB+P77759KLHfv3kX9+vVhamr6VK5HRE8Xl4So1oqKikJRURG++OILtWSlUuvWrTFlyhTxc3l5ORYtWoRWrVpBLpejRYsWeO+991BaWqp2XosWLTB48GD8+uuveOmll2BmZoaWLVviq6++EseEh4fD2dkZADBz5kzIZDK0aNECwIOllMo//1t4eDhkMplaW2JiInr06AFra2s0aNAArq6ueO+998T+hz3DkpSUhJ49e8LCwgLW1tYYOnQozp07V+31srKyMHbsWFhbW8PKygrjxo3D3bt3H/7F/sfo0aPx008/IT8/X2xLTU3FhQsXMHr06Crj8/LyMGPGDHh4eKBBgwawtLTEgAEDcOrUKXHMgQMH8OKLLwIAxo0bJy4tVd5nnz590K5dO6SlpaFXr16oX7+++L389xmWwMBAmJmZVbl/X19f2NjY4Pr16zW+VyLSHyYsVGvt3LkTLVu2RLdu3Wo0fvz48QgLC0OnTp2wYsUK9O7dG5GRkfD3968yNisrC6+99hpefvllLFu2DDY2Nhg7diwyMjIAAMOGDcOKFSsAAKNGjcKmTZvwySefaBR/RkYGBg8ejNLSUixcuBDLli3DK6+8gsOHDz/yvJ9//hm+vr7Izc1FeHg4QkNDceTIEXTv3h2XL1+uMn7EiBH4+++/ERkZiREjRiA2NhYRERE1jnPYsGGQyWT44YcfxLYtW7agbdu26NSpU5Xxly5dQnx8PAYPHozly5dj5syZOHPmDHr37i0mD25ubli4cCEAYOLEidi0aRM2bdqEXr16ifPcvn0bAwYMQIcOHfDJJ5+gb9++1ca3cuVK2NnZITAwEBUVFQCATz/9FPv27cOqVaugUChqfK9EpEcCUS1UUFAgABCGDh1ao/Hp6ekCAGH8+PFq7TNmzBAACElJSWKbs7OzAEBITk4W23JzcwW5XC5Mnz5dbMvOzhYACEuXLlWbMzAwUHB2dq4Sw4IFC4R//5VcsWKFAEC4efPmQ+OuvMaGDRvEtg4dOgj29vbC7du3xbZTp04JRkZGwpgxY6pc76233lKb89VXXxUaNWr00Gv++z4sLCwEQRCE1157TejXr58gCIJQUVEhODo6ChEREdV+ByUlJUJFRUWV+5DL5cLChQvFttTU1Cr3Vql3794CACEmJqbavt69e6u17d27VwAgLF68WLh06ZLQoEEDwc/P77H3SESGgxUWqpUKCwsBAA0bNqzR+N27dwMAQkND1dqnT58OAFWedXF3d0fPnj3Fz3Z2dnB1dcWlS5eeOOb/qnz25ccff4RKparROTdu3EB6ejrGjh0LW1tbsf2FF17Ayy+/LN7nv7399ttqn3v27Inbt2+L32FNjB49GgcOHIBSqURSUhKUSmW1y0HAg+dejIwe/E9PRUUFbt++LS53nThxosbXlMvlGDduXI3G+vj44H//+x8WLlyIYcOGwczMDJ9++mmNr0VE+seEhWolS0tLAMDff/9do/FXrlyBkZERWrdurdbu6OgIa2trXLlyRa29efPmVeawsbHBnTt3njDiqkaOHInu3btj/PjxcHBwgL+/P7Zt2/bI5KUyTldX1yp9bm5uuHXrFoqLi9Xa/3svNjY2AKDRvQwcOBANGzbE1q1bsXnzZrz44otVvstKKpUKK1asQJs2bSCXy9G4cWPY2dnh9OnTKCgoqPE1mzZtqtEDth9//DFsbW2Rnp6O6Oho2Nvb1/hcItI/JixUK1laWkKhUODs2bManfffh14fxtjYuNp2QRCe+BqVz1dUMjc3R3JyMn7++We8+eabOH36NEaOHImXX365ylhtaHMvleRyOYYNG4aNGzciLi7uodUVAPjggw8QGhqKXr164euvv8bevXuRmJiI559/vsaVJODB96OJkydPIjc3FwBw5swZjc4lIv1jwkK11uDBg3Hx4kWkpKQ8dqyzszNUKhUuXLig1p6Tk4P8/Hxxx48u2NjYqO2oqfTfKg4AGBkZoV+/fli+fDl+//13LFmyBElJSfjll1+qnbsyzszMzCp958+fR+PGjWFhYaHdDTzE6NGjcfLkSfz999/VPqhc6bvvvkPfvn3xxRdfwN/fHz4+PvD29q7yndQ0eayJ4uJijBs3Du7u7pg4cSKioqKQmpqqs/mJSHpMWKjWmjVrFiwsLDB+/Hjk5ORU6b948SJWrlwJ4MGSBoAqO3mWL18OABg0aJDO4mrVqhUKCgpw+vRpse3GjRuIi4tTG5eXl1fl3MoXqP13q3WlJk2aoEOHDti4caNaAnD27Fns27dPvE8p9O3bF4sWLcLq1avh6Oj40HHGxsZVqjfbt2/HX3/9pdZWmVhVl9xpavbs2bh69So2btyI5cuXo0WLFggMDHzo90hEhocvjqNaq1WrVtiyZQtGjhwJNzc3tTfdHjlyBNu3b8fYsWMBAO3bt0dgYCDWr1+P/Px89O7dG8eOHcPGjRvh5+f30C2zT8Lf3x+zZ8/Gq6++ismTJ+Pu3btYt24dnnvuObWHThcuXIjk5GQMGjQIzs7OyM3Nxdq1a9GsWTP06NHjofMvXboUAwYMgJeXF4KCgnDv3j2sWrUKVlZWCA8P19l9/JeRkRHef//9x44bPHgwFi5ciHHjxqFbt244c+YMNm/ejJYtW6qNa9WqFaytrRETE4OGDRvCwsICnp6ecHFx0SiupKQkrF27FgsWLBC3WW/YsAF9+vTB/PnzERUVpdF8RKQnet6lRCS5P/74Q5gwYYLQokULwdTUVGjYsKHQvXt3YdWqVUJJSYk4rqysTIiIiBBcXFyEevXqCU5OTsLcuXPVxgjCg23NgwYNqnKd/26nfdi2ZkEQhH379gnt2rUTTE1NBVdXV+Hrr7+usq15//79wtChQwWFQiGYmpoKCoVCGDVqlPDHH39UucZ/t/7+/PPPQvfu3QVzc3PB0tJSGDJkiPD777+rjam83n+3TW/YsEEAIGRnZz/0OxUE9W3ND/Owbc3Tp08XmjRpIpibmwvdu3cXUlJSqt2O/OOPPwru7u6CiYmJ2n327t1beP7556u95r/nKSwsFJydnYVOnToJZWVlauOmTZsmGBkZCSkpKY+8ByIyDDJB0ODJOiIiIiI94DMsREREZPCYsBAREZHBY8JCREREBo8JCxERERk8JixERERk8JiwEBERkcFjwkJEREQGr1a+6Tb1Us1/8ZWoLvFobqXvEIgMjtlT+DeheccQncxz7+RqnczzLGKFhYiIiAxeraywEBERGRQZ6wPaYsJCREQkNZlM3xE885iwEBERSY0VFq3xGyQiIiKDxwoLERGR1LgkpDUmLERERFLjkpDW+A0SERGRwWOFhYiISGpcEtIaExYiIiKpcUlIa/wGiYiIyOCxwkJERCQ1LglpjQkLERGR1LgkpDV+g0RERGTwWGEhIiKSGpeEtMYKCxERkdRkRro5NJScnIwhQ4ZAoVBAJpMhPj7+oWPffvttyGQyfPLJJ2rteXl5CAgIgKWlJaytrREUFISioiK1MadPn0bPnj1hZmYGJycnREVFVZl/+/btaNu2LczMzODh4YHdu3drdC9MWIiIiKQmk+nm0FBxcTHat2+PNWvWPHJcXFwcfvvtNygUiip9AQEByMjIQGJiIhISEpCcnIyJEyeK/YWFhfDx8YGzszPS0tKwdOlShIeHY/369eKYI0eOYNSoUQgKCsLJkyfh5+cHPz8/nD17tsb3IhMEQajx6GdE6qUCfYdAZJA8mlvpOwQig2P2FB6OMO8ZppN57h1a+MTnymQyxMXFwc/PT639r7/+gqenJ/bu3YtBgwZh6tSpmDp1KgDg3LlzcHd3R2pqKrp06QIA2LNnDwYOHIhr165BoVBg3bp1mDdvHpRKJUxNTQEAc+bMQXx8PM6fPw8AGDlyJIqLi5GQkCBet2vXrujQoQNiYmJqFD8rLERERFLT0ZJQaWkpCgsL1Y7S0tInDkulUuHNN9/EzJkz8fzzz1fpT0lJgbW1tZisAIC3tzeMjIxw9OhRcUyvXr3EZAUAfH19kZmZiTt37ohjvL291eb29fVFSkpKjWNlwkJERCQ1HSUskZGRsLKyUjsiIyOfOKyPPvoIJiYmmDx5crX9SqUS9vb2am0mJiawtbWFUqkUxzg4OKiNqfz8uDGV/TXBXUJERETPiLlz5yI0NFStTS6XP9FcaWlpWLlyJU6cOAHZM7CLiRUWIiIiqRnJdHLI5XJYWlqqHU+asBw6dAi5ublo3rw5TExMYGJigitXrmD69Olo0aIFAMDR0RG5ublq55WXlyMvLw+Ojo7imJycHLUxlZ8fN6ayvyaYsBAREUlNT9uaH+XNN9/E6dOnkZ6eLh4KhQIzZ87E3r17AQBeXl7Iz89HWlqaeF5SUhJUKhU8PT3FMcnJySgrKxPHJCYmwtXVFTY2NuKY/fv3q10/MTERXl5eNY6XS0JERES1VFFREbKyssTP2dnZSE9Ph62tLZo3b45GjRqpja9Xrx4cHR3h6uoKAHBzc0P//v0xYcIExMTEoKysDCEhIfD39xe3QI8ePRoREREICgrC7NmzcfbsWaxcuRIrVqwQ550yZQp69+6NZcuWYdCgQfj2229x/Phxta3Pj8MKCxERkdT09B6W48ePo2PHjujYsSMAIDQ0FB07dkRYWM23WW/evBlt27ZFv379MHDgQPTo0UMt0bCyssK+ffuQnZ2Nzp07Y/r06QgLC1N7V0u3bt2wZcsWrF+/Hu3bt8d3332H+Ph4tGvXrsZx8D0sRHUI38NCVNVTeQ+L94c6mefez3N0Ms+ziBUWIiIiMnh8hoWIiEhqz8C2YUPHhIWIiEhqOt7hUxcxYSEiIpIaKyxaY8pHREREBo8VFiIiIqlxSUhrTFiIiIikxiUhrTHlIyIiIoPHCgsREZHUuCSkNSYsREREUuOSkNaY8hEREZHBY4WFiIhIalwS0hoTFiIiIqkxYdEav0EiIiIyeKywEBERSY0P3WqNCQsREZHUuCSkNSYsREREUmOFRWtM+YiIiMjgscJCREQkNS4JaY0JCxERkdS4JKQ1pnxERERk8FhhISIikpiMFRatMWEhIiKSGBMW7XFJiIiIiAweKyxERERSY4FFa0xYiIiIJMYlIe1xSYiIiIgMHissREREEmOFRXtMWIiIiCTGhEV7TFiIiIgkxoRFe3yGhYiIiAweKyxERERSY4FFa0xYiIiIJMYlIe1xSYiIiIgMHissREREEmOFRXtMWIiIiCTGhEV7XBIiIiIig8cKCxERkcRYYdEeExYiIiKpMV/RGpeEiIiIaqnk5GQMGTIECoUCMpkM8fHxYl9ZWRlmz54NDw8PWFhYQKFQYMyYMbh+/braHHl5eQgICIClpSWsra0RFBSEoqIitTGnT59Gz549YWZmBicnJ0RFRVWJZfv27Wjbti3MzMzg4eGB3bt3a3QvTFiIiIgkJpPJdHJoqri4GO3bt8eaNWuq9N29excnTpzA/PnzceLECfzwww/IzMzEK6+8ojYuICAAGRkZSExMREJCApKTkzFx4kSxv7CwED4+PnB2dkZaWhqWLl2K8PBwrF+/Xhxz5MgRjBo1CkFBQTh58iT8/Pzg5+eHs2fP1vw7FARB0PgbMHCplwr0HQKRQfJobqXvEIgMjtlTeDjCbtxWncxzc8PIJz5XJpMhLi4Ofn5+Dx2TmpqKl156CVeuXEHz5s1x7tw5uLu7IzU1FV26dAEA7NmzBwMHDsS1a9egUCiwbt06zJs3D0qlEqampgCAOXPmID4+HufPnwcAjBw5EsXFxUhISBCv1bVrV3To0AExMTE1ip8VFiIiIonpqsJSWlqKwsJCtaO0tFRncRYUFEAmk8Ha2hoAkJKSAmtrazFZAQBvb28YGRnh6NGj4phevXqJyQoA+Pr6IjMzE3fu3BHHeHt7q13L19cXKSkpNY6NCQsREdEzIjIyElZWVmpHZGSkTuYuKSnB7NmzMWrUKFhaWgIAlEol7O3t1caZmJjA1tYWSqVSHOPg4KA2pvLz48ZU9tcEdwkRERFJTUe7hObOnYvQ0FC1NrlcrvW8ZWVlGDFiBARBwLp167SeTwpMWIiIiCSmq/ewyOVynSQo/1aZrFy5cgVJSUlidQUAHB0dkZubqza+vLwceXl5cHR0FMfk5OSojan8/Lgxlf01wSUhIiKiOqoyWblw4QJ+/vlnNGrUSK3fy8sL+fn5SEtLE9uSkpKgUqng6ekpjklOTkZZWZk4JjExEa6urrCxsRHH7N+/X23uxMREeHl51ThWJixEREQS09e25qKiIqSnpyM9PR0AkJ2djfT0dFy9ehVlZWV47bXXcPz4cWzevBkVFRVQKpVQKpW4f/8+AMDNzQ39+/fHhAkTcOzYMRw+fBghISHw9/eHQqEAAIwePRqmpqYICgpCRkYGtm7dipUrV6otXU2ZMgV79uzBsmXLcP78eYSHh+P48eMICQmp+XfIbc1EdQe3NRNV9TS2NTeZ+L1O5rmxfrhG4w8cOIC+fftWaQ8MDER4eDhcXFyqPe+XX35Bnz59ADx4cVxISAh27twJIyMjDB8+HNHR0WjQoIE4/vTp0wgODkZqaioaN26MSZMmYfbs2Wpzbt++He+//z4uX76MNm3aICoqCgMHDqzxvTBhIapDmLAQVVWbE5bahA/dEhERSYw/fqg9JixERERSY76iNT50S0RERAaPFRYiIiKJcUlIe0xYiIiIJMaERXtMWIiIiCTGhEV7fIaFiIiIDB4rLERERFJjgUVrTFiIiIgkxiUh7XFJiIiIiAweKyx1zM8J32H/rh9wM+cGAKCZswteHT0e7V/s9thzUw7sw5qP3kdnr16YFvaxpHEm7tyOXd99jYI7t9G8ZRuMeWcGWrk+L/Z/ER2JjJPHcCfvFszMzNHG/QX4vxUChVMLSeMi0saAl/8P16//VaV9pP9ovDd/gR4ioqeFFRbtMWGpY2wbO2DkuGA4NnWCIAg49PMuLF84A0tWb0Iz51YPPe9mznVs+Twaru06aB1DcmICkhMT8H5UTLX9vx1MxOb1n2DcpDlo7fo89sR/i4/en4yln22HlbUtAMCldVt07+uLRvaOKPq7ED98/Rk+mjcJKzbEw8jYWOsYiaSweet3UFVUiJ+zsi7gf+PH4WXf/nqMip4GJiza45JQHdOpa090eKk7HJs2R5Nmzhgx9l2YmdVH1vmzDz1HVVGBtVFhGP7mBNg7Nq3SX3b/PrZ8thKT3hiEIL9eWDB1HH4/nfbEMf4UtwV9B/iht88QNHVuiXGT5kAuN8PBfTvFMf838FW09egEOwcFXFq3xeuBb+P2zRyxckRkiGxtbdHYzk48kg/8Aien5ujy4kv6Do3I4Om1wnLr1i18+eWXSElJgVKpBAA4OjqiW7duGDt2LOzs7PQZXq2nqqjA0UP7UVpyD23aejx0XNyWL2BpZYM+vkOReTa9Sv/GdUvx19VsBM9ZDBtbOxw/cgBL35+CyHVb4Ni0uUYxlZeVIfvCeQwZESi2GRkZ4fkOLyLr3JlqzykpuYfkfTth56hAIzsHja5HpC9l9+9jV8IOvBk4jv/vuw7gP2Pt6S1hSU1Nha+vL+rXrw9vb28899xzAICcnBxER0fjww8/xN69e9GlSxd9hVhr/ZmdhfDQIJTdvw8zc3NMnR+Fps4tqx2beTYdB/buwAdrvq62/1auEsn7ErDyqx2wafQgwRz02hs4nZaCg4kJGDn2XY1i+7swHypVBaxsbNXarWxscePaFbW2xITv8O0Xq1Bacg9NmjljzpLVMKlXT6PrEelLUtLP+Pvvv/GK36v6DoWeBuYrWtNbwjJp0iS8/vrriImJqZJ5CoKAt99+G5MmTUJKSsoj5yktLUVpaala2/3SUpjK5TqPubZo0swZS9Z8jXvFRTj2axI+XRaB96NiqiQt9+4WI+bjBRg/5T00tLKudq4/L2dBparAjPGvqbWXl91HA0srAA+Smtn/Gyn2qSoqUF5RjqBXe4ttr4wci6H+4zS6j+59+8Oj40vIz7uFXd9vxqrI9xC27DOYmvKfPRm+uO+/R/cevWBvz6ogUU3oLWE5deoUYmNjqy2TyWQyTJs2DR07dnzsPJGRkYiIiFBrGz95NiZOmauzWGsbk3r14KhwAgC4tHHDpT9+x54ftyJosvp3lnvjL9zMuYFl4dPFNkFQAQDGDPLC0s+2o/TePRgZGWPRqq9gZKT+SJSZmTkAwKZRYyz5V4Xm+OFfkHr4F7wza6HY1qChJQCgoaU1jIyMUXAnT22ugjt5sLJppNZW36IB6ls0gGPT5mjd1gP/e70fjh85gG59fJ/oeyF6Wq5f/wtHfzuC5StX6TsUekq4JKQ9vSUsjo6OOHbsGNq2bVtt/7Fjx+Dg8Pj/5zF37lyEhoaqtZ35q0QnMdYVgqBCedn9Ku1NnJwRue4btbbvvlqHe3fv4s23p6ORnQNUqgqoVBUozM9D23bVJ5jGxiZiggQAlta2qGcqV2urZFKvHlzatEVGeiq6dOsDAFCpVMhIP46XX3n9EfcgQICA8rKymtwykV79GPcDbG0boWevPvoOhZ4SJiza01vCMmPGDEycOBFpaWno16+fmJzk5ORg//79+Oyzz/Dxx49/14dcLof8P8s/prcESWKuDbZuWIP2XbzQyN4RJXfv4siBvTh3+gRmLY4GAMR8vAA2jewxclwwTE3lcGqhvtW5vkVDABDbmzRzRre+/fHpx+EYPWEqnFs9h78L8pGRngonl9bo+FIPjWMc8OpofLosAi5t3NDq/29rLi29h94vDwbwoPLzW3IiPDp5oqGVDfJu5WLnto0wNZXX6H0yRPqkUqnwY9wPGDLUDyYmfLNEXcF8RXt6+9sSHByMxo0bY8WKFVi7di0q/v+7CYyNjdG5c2fExsZixIgR+gqv1irMz0PMxxHIz7uF+hYN4OTSGrMWR8OjkycA4FZuDmQyzXa7TwwNw4/ffIktn32CvNs30dDSGq3btnuiZAUAuvZ+GYUFd/D91+tRkHcbzq2ew6xFK8UloXqmpsg8m4498d+iuKgQVta2aNuuI8KWfyG+p4XIUP2WcgQ3blyH37Dh+g6F6JkiEwRB7+WIsrIy3Lp1CwDQuHFj1NNyp0fqpQJdhEVU63g0t9J3CEQGx+wp/F/3NjP36GSeC0vr7ksGDaIeWa9ePTRp0kTfYRAREUmCS0La45tuiYiIyOAZRIWFiIioNuMuIe0xYSEiIpIY8xXtcUmIiIiIDB4rLERERBIzMmKJRVtMWIiIiCTGJSHtcUmIiIiIDB4rLERERBLjLiHtMWEhIiKSGPMV7TFhISIikhgrLNrjMyxERERk8FhhISIikhgrLNpjwkJERCQx5iva45IQERERGTxWWIiIiCTGJSHtMWEhIiKSGPMV7XFJiIiIiAweExYiIiKJyWQynRyaSk5OxpAhQ6BQKCCTyRAfH6/WLwgCwsLC0KRJE5ibm8Pb2xsXLlxQG5OXl4eAgABYWlrC2toaQUFBKCoqUhtz+vRp9OzZE2ZmZnByckJUVFSVWLZv3462bdvCzMwMHh4e2L17t0b3woSFiIhIYjKZbg5NFRcXo3379lizZk21/VFRUYiOjkZMTAyOHj0KCwsL+Pr6oqSkRBwTEBCAjIwMJCYmIiEhAcnJyZg4caLYX1hYCB8fHzg7OyMtLQ1Lly5FeHg41q9fL445cuQIRo0ahaCgIJw8eRJ+fn7w8/PD2bNna/4dCoIgaP4VGLbUSwX6DoHIIHk0t9J3CEQGx+wpPM3ZZfEvOpnn+Pt9n/hcmUyGuLg4+Pn5AXhQXVEoFJg+fTpmzJgBACgoKICDgwNiY2Ph7++Pc+fOwd3dHampqejSpQsAYM+ePRg4cCCuXbsGhUKBdevWYd68eVAqlTA1NQUAzJkzB/Hx8Th//jwAYOTIkSguLkZCQoIYT9euXdGhQwfExMTUKH5WWIiIiCSmqyWh0tJSFBYWqh2lpaVPFFN2djaUSiW8vb3FNisrK3h6eiIlJQUAkJKSAmtrazFZAQBvb28YGRnh6NGj4phevXqJyQoA+Pr6IjMzE3fu3BHH/Ps6lWMqr1MTTFiIiIgkpqslocjISFhZWakdkZGRTxSTUqkEADg4OKi1Ozg4iH1KpRL29vZq/SYmJrC1tVUbU90c/77Gw8ZU9tcEtzUTERFJTFfvYZk7dy5CQ0PV2uRyuU7mNnRMWIiIiJ4RcrlcZwmKo6MjACAnJwdNmjQR23NyctChQwdxTG5urtp55eXlyMvLE893dHRETk6O2pjKz48bU9lfE1wSIiIikpi+dgk9iouLCxwdHbF//36xrbCwEEePHoWXlxcAwMvLC/n5+UhLSxPHJCUlQaVSwdPTUxyTnJyMsrIycUxiYiJcXV1hY2Mjjvn3dSrHVF6nJpiwEBERSUxf72EpKipCeno60tPTATx40DY9PR1Xr16FTCbD1KlTsXjxYuzYsQNnzpzBmDFjoFAoxJ1Ebm5u6N+/PyZMmIBjx47h8OHDCAkJgb+/PxQKBQBg9OjRMDU1RVBQEDIyMrB161asXLlSbelqypQp2LNnD5YtW4bz588jPDwcx48fR0hISI3vhUtCREREtdTx48fRt+8/W6Erk4jAwEDExsZi1qxZKC4uxsSJE5Gfn48ePXpgz549MDMzE8/ZvHkzQkJC0K9fPxgZGWH48OGIjo4W+62srLBv3z4EBwejc+fOaNy4McLCwtTe1dKtWzds2bIF77//Pt577z20adMG8fHxaNeuXY3vhe9hIapD+B4WoqqexntYukUl62SeI7N66WSeZxErLERERBLjrzVrj8+wEBERkcFjhYWIiEhiLLBojwkLERGRxLgkpD0uCREREZHBY4WFiIhIYqywaI8JCxERkcSYr2iPCQsREZHEWGHRHp9hISIiIoPHCgsREZHEWGDRHhMWIiIiiXFJSHtcEiIiIiKDxwoLERGRxFhg0R4TFiIiIokZMWPRGpeEiIiIyOCxwkJERCQxFli0x4SFiIhIYtwlpD0mLERERBIzYr6iNT7DQkRERAaPFRYiIiKJcUlIe0xYiIiIJMZ8RXtcEiIiIiKDp5OEJT8/XxfTEBER1UoyHf2nLtM4Yfnoo4+wdetW8fOIESPQqFEjNG3aFKdOndJpcERERLWBkUw3R12mccISExMDJycnAEBiYiISExPx008/YcCAAZg5c6bOAyQiIiLS+KFbpVIpJiwJCQkYMWIEfHx80KJFC3h6euo8QCIiomcddwlpT+MKi42NDf78808AwJ49e+Dt7Q0AEAQBFRUVuo2OiIioFpDJdHPUZRpXWIYNG4bRo0ejTZs2uH37NgYMGAAAOHnyJFq3bq3zAImIiIg0TlhWrFiBFi1a4M8//0RUVBQaNGgAALhx4wbeffddnQdIRET0rDOq6+URHZAJgiDoOwhdS71UoO8QiAySR3MrfYdAZHDMnsIrVId/maaTeb5/q7NO5nkW1egf044dO2o84SuvvPLEwRAREdVGfOhWezVKWPz8/Go0mUwm44O3REREpHM1SlhUKpXUcRAREdVaLLBoT6uVu5KSEpiZmekqFiIiolqJD91qT+P3sFRUVGDRokVo2rQpGjRogEuXLgEA5s+fjy+++ELnARIRERFpnLAsWbIEsbGxiIqKgqmpqdjerl07fP755zoNjoiIqDaQ6eioyzROWL766iusX78eAQEBMDY2Ftvbt2+P8+fP6zQ4IiKi2kAmk+nkqMs0Tlj++uuvat9oq1KpUFZWppOgiIiIiP5N44TF3d0dhw4dqtL+3XffoWPHjjoJioiIqDYxkunmqMs0TljCwsIQEhKCjz76CCqVCj/88AMmTJiAJUuWICwsTIoYiYiInmn6WBKqqKjA/Pnz4eLiAnNzc7Rq1QqLFi3Cv19wLwgCwsLC0KRJE5ibm8Pb2xsXLlxQmycvLw8BAQGwtLSEtbU1goKCUFRUpDbm9OnT6NmzJ8zMzODk5ISoqKgn/7IeQuOEZejQodi5cyd+/vlnWFhYICwsDOfOncPOnTvx8ssv6zxAIiIi0txHH32EdevWYfXq1Th37hw++ugjREVFYdWqVeKYqKgoREdHIyYmBkePHoWFhQV8fX1RUlIijgkICEBGRgYSExORkJCA5ORkTJw4UewvLCyEj48PnJ2dkZaWhqVLlyI8PBzr16/X6f3wt4SI6hD+lhBRVU/jt4Te3HxKJ/NsCmhf47GDBw+Gg4OD2itHhg8fDnNzc3z99dcQBAEKhQLTp0/HjBkzAAAFBQVwcHBAbGws/P39ce7cObi7uyM1NRVdunQBAOzZswcDBw7EtWvXoFAosG7dOsybNw9KpVLcPTxnzhzEx8frdDOOxhWWSsePH8emTZuwadMmpKXp5kediIiIaiNdLQmVlpaisLBQ7SgtLa32mt26dcP+/fvxxx9/AABOnTqFX3/9FQMGDAAAZGdnQ6lUwtvbWzzHysoKnp6eSElJAQCkpKTA2tpaTFYAwNvbG0ZGRjh69Kg4plevXmqvOvH19UVmZibu3Lmjs+9Q47zy2rVrGDVqFA4fPgxra2sAQH5+Prp164Zvv/0WzZo101lwREREtYGuHpiNjIxERESEWtuCBQsQHh5eZeycOXNQWFiItm3bwtjYGBUVFViyZAkCAgIAAEqlEgDg4OCgdp6Dg4PYp1QqYW9vr9ZvYmICW1tbtTEuLi5V5qjss7GxecK7VadxhWX8+PEoKyvDuXPnkJeXh7y8PJw7dw4qlQrjx4/XSVBERERU1dy5c1FQUKB2zJ07t9qx27Ztw+bNm7FlyxacOHECGzduxMcff4yNGzc+5ah1Q+MKy8GDB3HkyBG4urqKba6urli1ahV69uyp0+CIiIhqA1299E0ul0Mul9do7MyZMzFnzhz4+/sDADw8PHDlyhVERkYiMDAQjo6OAICcnBw0adJEPC8nJwcdOnQAADg6OiI3N1dt3vLycuTl5YnnOzo6IicnR21M5efKMbqgcYXFycmp2hfEVVRUQKFQ6CQoIiKi2kQfr+a/e/cujIzU/zVvbGwMlUoFAHBxcYGjoyP2798v9hcWFuLo0aPw8vICAHh5eSE/P1/tWdWkpCSoVCp4enqKY5KTk9Vyg8TERLi6uupsOQh4goRl6dKlmDRpEo4fPy62HT9+HFOmTMHHH3+ss8CIiIjoyQ0ZMgRLlizBrl27cPnyZcTFxWH58uV49dVXATyo+kydOhWLFy/Gjh07cObMGYwZMwYKhQJ+fn4AADc3N/Tv3x8TJkzAsWPHcPjwYYSEhMDf318sUowePRqmpqYICgpCRkYGtm7dipUrVyI0NFSn91Ojbc02NjZq5azi4mKUl5fDxOTBilLlny0sLJCXl6fTAJ8EtzUTVY/bmomqehrbmsdvPauTeT4f2a7GY//++2/Mnz8fcXFxyM3NhUKhwKhRoxAWFibu6BEEAQsWLMD69euRn5+PHj16YO3atXjuuefEefLy8hASEoKdO3fCyMgIw4cPR3R0NBo0aCCOOX36NIKDg5GamorGjRtj0qRJmD17tk7uuVKNEhZNHtAJDAzUKiBdYMJCVD0mLERVPY2EZcI23SQsn42oecJS29ToH5MhJCFERERUd2mVV5aUlOD+/ftqbZaWlloFREREVNvoapdQXabxQ7fFxcUICQmBvb09LCwsYGNjo3YQERGROplMN0ddpnHCMmvWLCQlJWHdunWQy+X4/PPPERERAYVCga+++kqKGImIiKiO03hJaOfOnfjqq6/Qp08fjBs3Dj179kTr1q3h7OyMzZs3i6/8JSIiogeM6np5RAc0rrDk5eWhZcuWAB48r1K5jblHjx5ITk7WbXRERES1AJeEtKdxwtKyZUtkZ2cDANq2bYtt27YBeFB5qfwxRCIiIvqHrn6tuS7TOGEZN24cTp06BeDBL0GuWbMGZmZmmDZtGmbOnKnzAImIiIhq9OK4R7ly5QrS0tLQunVrvPDCC7qKSysl5fqOgMgw2bwYou8QiAzOvZOrJb/GpLhzOpln1atuOpnnWaT1+/2cnZ3h7Oysi1iIiIhqpbq+nKMLNUpYoqOjazzh5MmTnzgYIiIiourUKGFZsWJFjSaTyWRMWIiIiP7DiAUWrdUoYancFURERESaY8KiPY13CRERERE9bU/hR7WJiIjqNj50qz0mLERERBLjkpD2uCREREREBo8VFiIiIolxRUh7T1RhOXToEN544w14eXnhr7/+AgBs2rQJv/76q06DIyIiqg2MZDKdHHWZxgnL999/D19fX5ibm+PkyZMoLS0FABQUFOCDDz7QeYBERETPOiMdHXWZxve/ePFixMTE4LPPPkO9evXE9u7du+PEiRM6DY6IiIgIeIJnWDIzM9GrV68q7VZWVsjPz9dFTERERLVKHV/N0QmNKyyOjo7Iysqq0v7rr7+iZcuWOgmKiIioNuEzLNrTOGGZMGECpkyZgqNHj0Imk+H69evYvHkzZsyYgXfeeUeKGImIiKiO03hJaM6cOVCpVOjXrx/u3r2LXr16QS6XY8aMGZg0aZIUMRIRET3T6nhxRCc0TlhkMhnmzZuHmTNnIisrC0VFRXB3d0eDBg2kiI+IiOiZxzfdau+JXxxnamoKd3d3XcZCREREVC2NE5a+ffs+8keckpKStAqIiIiotqnrD8zqgsYJS4cOHdQ+l5WVIT09HWfPnkVgYKCu4iIiIqo1mK9oT+OEZcWKFdW2h4eHo6ioSOuAiIiIiP5LZ2/6feONN/Dll1/qajoiIqJaw0imm6Mu09mvNaekpMDMzExX0xEREdUaMtTxbEMHNE5Yhg0bpvZZEATcuHEDx48fx/z583UWGBERUW1R16sjuqBxwmJlZaX22cjICK6urli4cCF8fHx0FhgRERFRJY0SloqKCowbNw4eHh6wsbGRKiYiIqJahRUW7Wn00K2xsTF8fHz4q8xEREQakMlkOjnqMo13CbVr1w6XLl2SIhYiIiKiammcsCxevBgzZsxAQkICbty4gcLCQrWDiIiI1HFbs/Zq/AzLwoULMX36dAwcOBAA8Morr6iVpwRBgEwmQ0VFhe6jJCIieobV8dUcnahxhSUiIgLFxcX45ZdfxCMpKUk8Kj8TERGRYfjrr7/wxhtvoFGjRjA3N4eHhweOHz8u9guCgLCwMDRp0gTm5ubw9vbGhQsX1ObIy8tDQEAALC0tYW1tjaCgoCpvtj99+jR69uwJMzMzODk5ISoqSuf3UuMKiyAIAIDevXvrPAgiIqLaTB8/fnjnzh10794dffv2xU8//QQ7OztcuHBBbZdvVFQUoqOjsXHjRri4uGD+/Pnw9fXF77//Lr4MNiAgADdu3EBiYiLKysowbtw4TJw4EVu2bAEAFBYWwsfHB97e3oiJicGZM2fw1ltvwdraGhMnTtTZ/ciEykzkMYyMjJCTkwM7OzudXVwqJeX6joDIMNm8GKLvEIgMzr2TqyW/RvSv2TqZZ3IPlxqPnTNnDg4fPoxDhw5V2y8IAhQKBaZPn44ZM2YAAAoKCuDg4IDY2Fj4+/vj3LlzcHd3R2pqKrp06QIA2LNnDwYOHIhr165BoVBg3bp1mDdvHpRKJUxNTcVrx8fH4/z581re8T80euj2ueeeg62t7SMPIiIikkZpaWmVzS6lpaXVjt2xYwe6dOmC119/Hfb29ujYsSM+++wzsT87OxtKpRLe3t5im5WVFTw9PZGSkgLgwc/uWFtbi8kKAHh7e8PIyAhHjx4Vx/Tq1UtMVgDA19cXmZmZuHPnjs7uXaMXx0VERFR50y0RERE9mq5WhCIjIxEREaHWtmDBAoSHh1cZe+nSJaxbtw6hoaF47733kJqaismTJ8PU1BSBgYFQKpUAAAcHB7XzHBwcxD6lUgl7e3u1fhMTE9ja2qqNcXFxqTJHZZ+uXjSrUcLi7+9fJXAiIiJ6NCMd/fjh3LlzERoaqtYml8urHatSqdClSxd88MEHAICOHTvi7NmziImJQWBgoE7ieZpqvCRU19+wR0RE9KRkMt0ccrkclpaWasfDEpYmTZrA3d1drc3NzQ1Xr14FADg6OgIAcnJy1Mbk5OSIfY6OjsjNzVXrLy8vR15entqY6ub49zV0ocYJSw2fzSUiIiID0L17d2RmZqq1/fHHH3B2dgYAuLi4wNHREfv37xf7CwsLcfToUXh5eQEAvLy8kJ+fj7S0NHFMUlISVCoVPD09xTHJyckoKysTxyQmJsLV1VWnvztY44RFpVJxOYiIiOgJ6ONNt9OmTcNvv/2GDz74AFlZWdiyZQvWr1+P4OBgAA9WTqZOnYrFixdjx44dOHPmDMaMGQOFQgE/Pz8ADyoy/fv3x4QJE3Ds2DEcPnwYISEh8Pf3h0KhAACMHj0apqamCAoKQkZGBrZu3YqVK1dWWbrSlkbPsBAREZHm9PEelhdffBFxcXGYO3cuFi5cCBcXF3zyyScICAgQx8yaNQvFxcWYOHEi8vPz0aNHD+zZs0d8BwsAbN68GSEhIejXrx+MjIwwfPhwREdHi/1WVlbYt28fgoOD0blzZzRu3BhhYWE6fQcLoMF7WJ4lfA8LUfX4Hhaiqp7Ge1jW/3ZFJ/NM7Oqsk3meRaywEBERSYz7VrTHhIWIiEhi+lgSqm00etMtERERkT6wwkJERCQxFli0x4SFiIhIYlzO0B6/QyIiIjJ4rLAQERFJjD9voz0mLERERBJjuqI9JixEREQS47Zm7fEZFiIiIjJ4rLAQERFJjPUV7TFhISIikhhXhLTHJSEiIiIyeKywEBERSYzbmrXHhIWIiEhiXM7QHr9DIiIiMnissBAREUmMS0LaY8JCREQkMaYr2uOSEBERERk8VliIiIgkxiUh7TFhISIikhiXM7THhIWIiEhirLBoj0kfERERGTxWWIiIiCTG+or2mLAQERFJjCtC2uOSEBERERk8VliIiIgkZsRFIa0xYSEiIpIYl4S0xyUhIiIiMnissBAREUlMxiUhrTFhISIikhiXhLTHJSEiIiIyeKywEBERSYy7hLTHhIWIiEhiXBLSHhMWIiIiiTFh0R6fYSEiIiKDxwoLERGRxLitWXtMWIiIiCRmxHxFa1wSIiIiIoPHhIWIiEhiMh39RxsffvghZDIZpk6dKraVlJQgODgYjRo1QoMGDTB8+HDk5OSonXf16lUMGjQI9evXh729PWbOnIny8nK1MQcOHECnTp0gl8vRunVrxMbGahVrdZiwEBERSUwm083xpFJTU/Hpp5/ihRdeUGufNm0adu7cie3bt+PgwYO4fv06hg0bJvZXVFRg0KBBuH//Po4cOYKNGzciNjYWYWFh4pjs7GwMGjQIffv2RXp6OqZOnYrx48dj7969Tx5wNWSCIAg6ndEAlJQ/fgxRXWTzYoi+QyAyOPdOrpb8Gr9k3tbJPH1dG2l8TlFRETp16oS1a9di8eLF6NChAz755BMUFBTAzs4OW7ZswWuvvQYAOH/+PNzc3JCSkoKuXbvip59+wuDBg3H9+nU4ODgAAGJiYjB79mzcvHkTpqammD17Nnbt2oWzZ8+K1/T390d+fj727Nmjk/sGWGEhIiKSnK6WhEpLS1FYWKh2lJaWPvLawcHBGDRoELy9vdXa09LSUFZWptbetm1bNG/eHCkpKQCAlJQUeHh4iMkKAPj6+qKwsBAZGRnimP/O7evrK86hK0xYiIiIJGYk080RGRkJKysrtSMyMvKh1/32229x4sSJascolUqYmprC2tpard3BwQFKpVIc8+9kpbK/su9RYwoLC3Hv3j2Nv6uH4bZmIiKiZ8TcuXMRGhqq1iaXy6sd++eff2LKlClITEyEmZnZ0whPUqywkCRycnIwd/YM9OrmiZc6vYDhfkOQcfaMvsMieqjunVrhu0/+h0v7luDeydUY0ueFR47v2bkN7p1cXeVwaNRQ0jiHeXdE+g/v485vK5C67T349nB/6Njoef64d3I1Qkb3kTQmejxdLQnJ5XJYWlqqHQ9LWNLS0pCbm4tOnTrBxMQEJiYmOHjwIKKjo2FiYgIHBwfcv38f+fn5aufl5OTA0dERAODo6Fhl11Dl58eNsbS0hLm5uS6+PgBMWEgChQUFGPvGKJiY1MOamM/ww45dmD5zNiwtrfQdGtFDWZjLceaPvzA1cqtG53kMXYgW3nPFIzev6Ilj6Nm5Dc7vinhof9f2LtgYORYb41PQddSH2HngFLYtnwj3Vk2qjH2l7wt4yaMFrufmP3E8pDv62CXUr18/nDlzBunp6eLRpUsXBAQEiH+uV68e9u/fL56TmZmJq1evwsvLCwDg5eWFM2fOIDc3VxyTmJgIS0tLuLu7i2P+PUflmMo5dIVLQqRzX37xGRwcHbFoyT9rps2aOekxIqLH23f4d+w7/LvG593M+xsFRdWv08tkMkwf9zKChnWDQyNLXLiaiw8/24O4n9OfKMbgUX2w78g5rPjqwb8cFq7dhX6ebfG2f29MXvKtOE5hZ4Xls1/HkHfXIG7VO090LdItfbzotmHDhmjXrp1am4WFBRo1aiS2BwUFITQ0FLa2trC0tMSkSZPg5eWFrl27AgB8fHzg7u6ON998E1FRUVAqlXj//fcRHBwsVnbefvttrF69GrNmzcJbb72FpKQkbNu2Dbt27dLp/TBhIZ07+EsSunXvgRnTJuP48VTY2ztgpP9oDH99hL5DI9K5o1vnwLSeCX6/eANLYnYj5dQlsW/mWz4YNfBFTFqyFVlXc9GjU2t8uTgQN+8U4de0LI2v5fmCC6K/TlJrS0w5hyF9/1m+kslk+GLxGKzYuB/nLimf/MaoTlixYgWMjIwwfPhwlJaWwtfXF2vXrhX7jY2NkZCQgHfeeQdeXl6wsLBAYGAgFi5cKI5xcXHBrl27MG3aNKxcuRLNmjXD559/Dl9fX53GatAJy59//okFCxbgyy+/fOiY0tLSKlu6BGP5Q9f0SHrXrv2JbVu/wZuB4xA08W1knDmDjyIXo169enjF71V9h0ekE8pbBQhZ/A1O/H4VclMTjPXrhr2fTUGvMUuRfv4aTOuZYFaQDwa9vRpHT2cDAC7/dRvdOrbC+OE9nihhcWhsidy8v9Xacm//DYdGluLn6eNeRnmFCmu+OaDV/ZFuGWnz1jcdOnDggNpnMzMzrFmzBmvWrHnoOc7Ozti9e/cj5+3Tpw9OnjypixAfyqATlry8PGzcuPGRCUtkZCQiItTXfOfNX4D3w8Iljo4eRqUS8Hy7dpg89cGT7G5u7sjKuoDt275lwkK1xoUrubhw5Z91/d9OZaOlU2NMCvg/BM3/Cq2cGsPCXI6Edeov6zOtZ4xT56+Jn28eXib+2dhIBrmpiVrbN7tT1ZZ7HqWjmxOCR/VBt9EfPeltkUQMI115tuk1YdmxY8cj+y9duvTIfqD6LV6CMasr+mRnZ4eWrVqptbVs2RI/J+r2Nc1Ehub42Svo1vHBf/cb1H/wv0OvTl5X5cHX+/f/eR23p/8/z3q91K4FFk8ZCp8JK8W2v4tKxD/n3CqEva36LiT7Rg2Rc7sQANC9YyvY2zbAH7v/KdebmBjjw9BhCAnoi7aDFmh5h0T6o9eExc/PDzKZDI/6dQDZY8pocnnV5R++ml+/OnTshMvZ2WptVy5fhkLRVE8RET0dL7g2g/JmAQDg3CUlSkrL4ORo88jln0t/3hL/3NTeBuUVKrW2fzt6Oht9XnLF6i0HxLZ+Xdvi6OnLAIAtu1KRdDRT7Zyda4OxZdcxfPXjb094V6QTLLFoTa8JS5MmTbB27VoMHTq02v709HR07tz5KUdF2npjTCAC3xiFz9fHwMd3AM6eOY3vvtuGsPCFjz+ZSE8szE3RyslO/NyiaSO88FxT3Cm8iz+Vd7Bw0itQ2Fth/PxNAICQ0X1w+fpt/H7xBsxM62Hcq93Q58XnMPjdB79LU3S3FJ98tR9R04fDyMgIR05ehFUDM3h1aIXC4hJs3nlU4xjXfHMA+z6biilv/h9+OpSB1307o5N7cwQv+gYAkFdQjLyCYrVzysorkHOrUG35ip4+bX9pmfScsHTu3BlpaWkPTVgeV30hw9TO4wUsX7ka0Z8sx6fr1qBps2aYNfs9DBr8ir5DI3qoTu7O2Pf5FPFz1IzhAIBNO37DxAVfw7GxJZwcbcV+03om+HDaMCjsrXC3pAxnL/yFgW+vQvLxC+KYiLUJuHWnCDPHvQyX+aOQ//c9pJ/7E1FfPtny6G+nsjH2vVgsCB6MiJAhyLp6EyNC1+P3izee8K6Jnh16/bXmQ4cOobi4GP3796+2v7i4GMePH0fv3r01mpdLQkTV4681E1X1NH6t+dilAp3M81LLuvsCTr1WWHr27PnIfgsLC42TFSIiIkPDBSHt8dX8REREZPAM+j0sREREtQJLLFpjwkJERCQx7hLSHhMWIiIiiRnIm/mfaXyGhYiIiAweKyxEREQSY4FFe0xYiIiIpMaMRWtcEiIiIiKDxwoLERGRxLhLSHtMWIiIiCTGXULa45IQERERGTxWWIiIiCTGAov2mLAQERFJjRmL1rgkRERERAaPFRYiIiKJcZeQ9piwEBERSYy7hLTHhIWIiEhizFe0x2dYiIiIyOCxwkJERCQ1lli0xoSFiIhIYnzoVntcEiIiIiKDxwoLERGRxLhLSHtMWIiIiCTGfEV7XBIiIiIig8cKCxERkdRYYtEaExYiIiKJcZeQ9rgkRERERAaPFRYiIiKJcZeQ9piwEBERSYz5ivaYsBAREUmNGYvW+AwLERERGTxWWIiIiCTGXULaY4WFiIhIYjKZbg5NREZG4sUXX0TDhg1hb28PPz8/ZGZmqo0pKSlBcHAwGjVqhAYNGmD48OHIyclRG3P16lUMGjQI9evXh729PWbOnIny8nK1MQcOHECnTp0gl8vRunVrxMbGPsnX9EhMWIiIiGqhgwcPIjg4GL/99hsSExNRVlYGHx8fFBcXi2OmTZuGnTt3Yvv27Th48CCuX7+OYcOGif0VFRUYNGgQ7t+/jyNHjmDjxo2IjY1FWFiYOCY7OxuDBg1C3759kZ6ejqlTp2L8+PHYu3evTu9HJgiCoNMZDUBJ+ePHENVFNi+G6DsEIoNz7+Rqya9xMfeeTuZpZW/+xOfevHkT9vb2OHjwIHr16oWCggLY2dlhy5YteO211wAA58+fh5ubG1JSUtC1a1f89NNPGDx4MK5fvw4HBwcAQExMDGbPno2bN2/C1NQUs2fPxq5du3D27FnxWv7+/sjPz8eePXu0u+F/YYWFiIhIajLdHKWlpSgsLFQ7SktLaxRCQUEBAMDW1hYAkJaWhrKyMnh7e4tj2rZti+bNmyMlJQUAkJKSAg8PDzFZAQBfX18UFhYiIyNDHPPvOSrHVM6hK0xYiIiInhGRkZGwsrJSOyIjIx97nkqlwtSpU9G9e3e0a9cOAKBUKmFqagpra2u1sQ4ODlAqleKYfycrlf2VfY8aU1hYiHv3dFNZArhLiIiISHK62iU0d+5chIaGqrXJ5fLHnhccHIyzZ8/i119/1Ukc+sCEhYiISGK6ejW/XC6vUYLybyEhIUhISEBycjKaNWsmtjs6OuL+/fvIz89Xq7Lk5OTA0dFRHHPs2DG1+Sp3Ef17zH93FuXk5MDS0hLm5k/+zM1/cUmIiIioFhIEASEhIYiLi0NSUhJcXFzU+jt37ox69eph//79YltmZiauXr0KLy8vAICXlxfOnDmD3NxccUxiYiIsLS3h7u4ujvn3HJVjKufQFVZYiIiIJKaP18YFBwdjy5Yt+PHHH9GwYUPxmRMrKyuYm5vDysoKQUFBCA0Nha2tLSwtLTFp0iR4eXmha9euAAAfHx+4u7vjzTffRFRUFJRKJd5//30EBweLlZ63334bq1evxqxZs/DWW28hKSkJ27Ztw65du3R6P9zWTFSHcFszUVVPY1vz5dslOpmnRSOzGo+VPWQdasOGDRg7diyABy+Omz59Or755huUlpbC19cXa9euFZd7AODKlSt45513cODAAVhYWCAwMBAffvghTEz+qXkcOHAA06ZNw++//45mzZph/vz54jV0hQkLUR3ChIWoqqeRsFy5XbOtx4/j3Eiz51dqEz7DQkRERAaPz7AQERFJTFe7hOoyJixEREQSY76iPS4JERERkcFjhYWIiEhiXBLSHhMWIiIiyTFj0RaXhIiIiMjgscJCREQkMS4JaY8JCxERkcSYr2iPS0JERERk8FhhISIikhiXhLTHhIWIiEhiMi4KaY0JCxERkdSYr2iNz7AQERGRwWOFhYiISGIssGiPCQsREZHE+NCt9rgkRERERAaPFRYiIiKJcZeQ9piwEBERSY35ita4JEREREQGjxUWIiIiibHAoj0mLERERBLjLiHtcUmIiIiIDB4rLERERBLjLiHtMWEhIiKSGJeEtMclISIiIjJ4TFiIiIjI4HFJiIiISGJcEtIeExYiIiKJ8aFb7XFJiIiIiAweKyxEREQS45KQ9piwEBERSYz5iva4JEREREQGjxUWIiIiqbHEojUmLERERBLjLiHtcUmIiIiIDB4rLERERBLjLiHtMWEhIiKSGPMV7TFhISIikhozFq3xGRYiIiIyeKywEBERSYy7hLTHhIWIiEhifOhWe1wSIiIiIoMnEwRB0HcQVDuVlpYiMjISc+fOhVwu13c4RAaDfzeINMeEhSRTWFgIKysrFBQUwNLSUt/hEBkM/t0g0hyXhIiIiMjgMWEhIiIig8eEhYiIiAweExaSjFwux4IFC/hQIdF/8O8Gkeb40C0REREZPFZYiIiIyOAxYSEiIiKDx4SFiIiIDB4TFiIiIjJ4TFhIMmvWrEGLFi1gZmYGT09PHDt2TN8hEelVcnIyhgwZAoVCAZlMhvj4eH2HRPTMYMJCkti6dStCQ0OxYMECnDhxAu3bt4evry9yc3P1HRqR3hQXF6N9+/ZYs2aNvkMheuZwWzNJwtPTEy+++CJWr14NAFCpVHBycsKkSZMwZ84cPUdHpH8ymQxxcXHw8/PTdyhEzwRWWEjn7t+/j7S0NHh7e4ttRkZG8Pb2RkpKih4jIyKiZxUTFtK5W7duoaKiAg4ODmrtDg4OUCqVeoqKiIieZUxYiIiIyOAxYSGda9y4MYyNjZGTk6PWnpOTA0dHRz1FRUREzzImLKRzpqam6Ny5M/bv3y+2qVQq7N+/H15eXnqMjIiInlUm+g6AaqfQ0FAEBgaiS5cueOmll/DJJ5+guLgY48aN03doRHpTVFSErKws8XN2djbS09Nha2uL5s2b6zEyIsPHbc0kmdWrV2Pp0qVQKpXo0KEDoqOj4enpqe+wiPTmwIED6Nu3b5X2wMBAxMbGPv2AiJ4hTFiIiIjI4PEZFiIiIjJ4TFiIiIjI4DFhISIiIoPHhIWIiIgMHhMWIiIiMnhMWIiIiMjgMWEhIiIig8eEhUiPxo4dCz8/P/Fznz59MHXq1Kcex4EDByCTyZCfn//QMTKZDPHx8TWeMzw8HB06dNAqrsuXL0MmkyE9PV2reYjo2ceEheg/xo4dC5lMBplMBlNTU7Ru3RoLFy5EeXm55Nf+4YcfsGjRohqNrUmSQURUW/C3hIiq0b9/f2zYsAGlpaXYvXs3goODUa9ePcydO7fK2Pv378PU1FQn17W1tdXJPEREtQ0rLETVkMvlcHR0hLOzM9555x14e3tjx44dAP5ZxlmyZAkUCgVcXV0BAH/++SdGjBgBa2tr2NraYujQobh8+bI4Z0VFBUJDQ2FtbY1GjRph1qxZ+O8vY/x3Sai0tBSzZ8+Gk5MT5HI5WrdujS+++AKXL18Wf5PGxsYGMpkMY8eOBfDgl7EjIyPh4uICc3NztG/fHt99953adXbv3o3nnnsO5ubm6Nu3r1qcNTV79mw899xzqF+/Plq2bIn58+ejrKysyrhPP/0UTk5OqF+/PkaMGIGCggK1/s8//xxubm4wMzND27ZtsXbt2ode886dOwgICICdnR3Mzc3Rpk0bbNiwQePYiejZwwoLUQ2Ym5vj9u3b4uf9+/fD0tISiYmJAICysjL4+vrCy8sLhw4dgomJCRYvXoz+/fvj9OnTMDU1xbJlyxAbG4svv/wSbm5uWLZsGeLi4vB///d/D73umDFjkJKSgujoaLRv3x7Z2dm4desWnJyc8P3332P48OHIzMyEpaUlzM3NAQCRkZH4+uuvERMTgzZt2iA5ORlvvPEG7Ozs0Lt3b/z5558YNmwYgoODMXHiRBw/fhzTp0/X+Dtp2LAhYmNjoVAocObMGUyYMAENGzbErFmzxDFZWVnYtm0bdu7cicLCQgQFBeHdd9/F5s2bAQCbN29GWFgYVq9ejY4dO+LkyZOYMGECLCwsEBgYWOWa8+fPx++//46ffvoJjRs3RlZWFu7du6dx7ET0DBKISE1gYKAwdOhQQRAEQaVSCYmJiYJcLhdmzJgh9js4OAilpaXiOZs2bRJcXV0FlUoltpWWlgrm5ubC3r17BUEQhCZNmghRUVFif1lZmdCsWTPxWoIgCL179xamTJkiCIIgZGZmCgCExMTEauP85ZdfBADCnTt3xLaSkhKhfv36wpEjR9TGBgUFCaNGjRIEQRDmzp0ruLu7q/XPnj27ylz/BUCIi4t7aP/SpUuFzp07i58XLFggGBsbC9euXRPbfvrpJ8HIyEi4ceOGIAiC0KpVK2HLli1q8yxatEjw8vISBEEQsrOzBQDCyZMnBUEQhCFDhgjjxo17aAxEVHuxwkJUjYSEBDRo0ABlZWVQqVQYPXo0wsPDxX4PDw+151ZOnTqFrKwsNGzYUG2ekpISXLx4EQUFBbhx4wY8PT3FPhMTE3Tp0qXKslCl9PR0GBsbo3fv3jWOOysrC3fv3sXLL7+s1n7//n107NgRAHDu3Dm1OADAy8urxteotHXrVkRHR+PixYsoKipCeXk5LC0t1cY0b94cTZs2VbuOSqVCZmYmGjZsiIsXLyIoKAgTJkwQx5SXl8PKyqraa77zzjsYPnw4Tpw4AR8fH/j5+aFbt24ax05Ezx4mLETV6Nu3L9atWwdTU1MoFAqYmKj/VbGwsFD7XFRUhM6dO4tLHf9mZ2f3RDFULvFooqioCACwa9cutUQBePBcjq6kpKQgICAAERER8PX1hZWVFb799lssW7ZM41g/++yzKgmUsbFxtecMGDAAV65cwe7du5GYmIh+/fohODgYH3/88ZPfDBE9E5iwEFXDwsICrVu3rvH4Tp06YevWrbC3t69SZajUpEkTHD16FL169QLwoJKQlpaGTp06VTvew8MDKpUKBw8ehLe3d5X+ygpPRUWF2Obu7g65XI6rV68+tDLj5uYmPkBc6bfffnv8Tf7LkSNH4OzsjHnz5oltV65cqTLu6tWruH79OhQKhXgdIyMjuLq6wsHBAQqFApcuXUJAQECNr21nZ4fAwEAEBgaiZ8+emDlzJhMWojqAu4SIdCAgIACNGzfG0KFDcejQIWRnZ+PAgQOYPHkyrl27BgCYMmUKPvzwQ8THx+P8+fN49913H/kOlRYtWiAwMBBvvfUW4uPjxTm3bdsGAHB2doZMJkNCQgJu3ryJoqIiNGzYEDNmzMC0adOwceNGXLx4ESdOnMCqVauwceNGAMDbb7+NCxcuYObMmcjMzMSWLVsQGxur0f22adMGV69exbfffouLFy8iOjoacXFxVcaZmZkhMDAQp06dwqFDhzB58mSMGDECjo6OAICIiAhERkYiOjoaf/zxB86cOYMNGzZg+fLl1V43LCwMP/74I7KyspCRkYGEhAS4ublpFDsRPZuYsBDpQP369ZGcnIzmzZtj2LBhcHNzQ1BQEEpKSsSKy/Tp0/Hmm28iMDAQXl5eaNiwIV599dVHzrtu3Tq89tprePfdd9G2bVtMmDABxcXFAICmTZsiIiICc+bMgYODA0JCQgAAixYtwvz58xEZGQk3Nzf0798fu3btgouLC4AHz5V8//33iI+PR/v27RETE4MPPvhAo/t95ZVXMG3aNISEhKBDhw44cuQI5s+fX2Vc69atMWzYMAwcOBA+Pj544YUX1LYtjx8/Hp9//jk2bNgADw8P9O7dG7GxsWKs/2Vqaoq5c+fihRdeQK9evWBsbIxvv/1Wo9iJ6NkkEx72xB8RERGRgWCFhYiIiAweExYiIiIyeExYiIiIyOAxYSEiIiKDx4SFiIiIDB4TFiIiIjJ4TFiIiIjI4DFhISIiIoPHhIWIiIgMHhMWIiIiMnhMWIiIiMjgMWEhIiIig/f/AACxRtgVXT4LAAAAAElFTkSuQmCC",
      "text/plain": [
       "<Figure size 640x480 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from sklearn.metrics import roc_curve, auc\n",
    "\n",
    "# Plot the ROC curve\n",
    "y_pred_proba = best_pipeline.predict_proba(X)[:, 1]\n",
    "fpr, tpr, _ = roc_curve(y, y_pred_proba)\n",
    "auc_value = auc(fpr, tpr)\n",
    "\n",
    "plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % auc_value)\n",
    "plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')\n",
    "plt.xlim([0.0, 1.0])\n",
    "plt.ylim([0.0, 1.05])\n",
    "plt.xlabel('False Positive Rate')\n",
    "plt.ylabel('True Positive Rate')\n",
    "plt.title('ROC Curve')\n",
    "plt.legend(loc=\"lower right\")\n",
    "plt.show()\n",
    "\n",
    "# Plot the confusion matrix\n",
    "cm = confusion_matrix(y, y_pred)\n",
    "sns.heatmap(cm, annot=True, cmap='Blues')\n",
    "plt.xlabel('Predicted labels')\n",
    "plt.ylabel('True labels')\n",
    "plt.title('Confusion Matrix')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:15:27.288215Z",
     "iopub.status.busy": "2024-09-25T09:15:27.287789Z",
     "iopub.status.idle": "2024-09-25T09:15:45.781113Z",
     "shell.execute_reply": "2024-09-25T09:15:45.780141Z",
     "shell.execute_reply.started": "2024-09-25T09:15:27.288181Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-2 {color: black;background-color: white;}#sk-container-id-2 pre{padding: 0;}#sk-container-id-2 div.sk-toggleable {background-color: white;}#sk-container-id-2 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-2 label.sk-toggleable__label-arrow:before {content: \"▸\";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-2 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-2 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-2 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-2 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-2 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-2 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: \"▾\";}#sk-container-id-2 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-2 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-2 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-2 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-2 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-2 div.sk-parallel-item::after {content: \"\";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-2 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-2 div.sk-serial::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-2 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-2 div.sk-item {position: relative;z-index: 1;}#sk-container-id-2 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-2 div.sk-item::before, #sk-container-id-2 div.sk-parallel-item::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-2 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-2 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-2 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-2 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-2 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-2 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-2 div.sk-label-container {text-align: center;}#sk-container-id-2 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-2 div.sk-text-repr-fallback {display: none;}</style><div id=\"sk-container-id-2\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>Pipeline(steps=[(&#x27;preprocessor&#x27;,\n",
       "                 ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  (&#x27;scaler&#x27;,\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  [&#x27;votes&#x27;,\n",
       "                                                   &#x27;approx_cost(for two &#x27;\n",
       "                                                   &#x27;people)&#x27;,\n",
       "                                                   &#x27;online_order_encoded&#x27;,\n",
       "                                                   &#x27;book_table_encoded&#x27;]),\n",
       "                                                 (&#x27;cat&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                                  (&#x27;encoder&#x27;,\n",
       "                                                                   OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                                  [&#x27;location&#x27;, &#x27;rest_type&#x27;,\n",
       "                                                   &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;,\n",
       "                                                   &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                                   &#x27;listed_in(type)&#x27;,\n",
       "                                                   &#x27;listed_in(city)&#x27;])])),\n",
       "                (&#x27;model&#x27;, RandomForestClassifier())])</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item sk-dashed-wrapped\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-10\" type=\"checkbox\" ><label for=\"sk-estimator-id-10\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">Pipeline</label><div class=\"sk-toggleable__content\"><pre>Pipeline(steps=[(&#x27;preprocessor&#x27;,\n",
       "                 ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  (&#x27;scaler&#x27;,\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  [&#x27;votes&#x27;,\n",
       "                                                   &#x27;approx_cost(for two &#x27;\n",
       "                                                   &#x27;people)&#x27;,\n",
       "                                                   &#x27;online_order_encoded&#x27;,\n",
       "                                                   &#x27;book_table_encoded&#x27;]),\n",
       "                                                 (&#x27;cat&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                                  (&#x27;encoder&#x27;,\n",
       "                                                                   OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                                  [&#x27;location&#x27;, &#x27;rest_type&#x27;,\n",
       "                                                   &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;,\n",
       "                                                   &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                                   &#x27;listed_in(type)&#x27;,\n",
       "                                                   &#x27;listed_in(city)&#x27;])])),\n",
       "                (&#x27;model&#x27;, RandomForestClassifier())])</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item sk-dashed-wrapped\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-11\" type=\"checkbox\" ><label for=\"sk-estimator-id-11\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">preprocessor: ColumnTransformer</label><div class=\"sk-toggleable__content\"><pre>ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                 Pipeline(steps=[(&#x27;imputer&#x27;, SimpleImputer()),\n",
       "                                                 (&#x27;scaler&#x27;, StandardScaler())]),\n",
       "                                 [&#x27;votes&#x27;, &#x27;approx_cost(for two people)&#x27;,\n",
       "                                  &#x27;online_order_encoded&#x27;,\n",
       "                                  &#x27;book_table_encoded&#x27;]),\n",
       "                                (&#x27;cat&#x27;,\n",
       "                                 Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                  SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                 (&#x27;encoder&#x27;,\n",
       "                                                  OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                 [&#x27;location&#x27;, &#x27;rest_type&#x27;, &#x27;dish_liked&#x27;,\n",
       "                                  &#x27;cuisines&#x27;, &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                  &#x27;listed_in(type)&#x27;, &#x27;listed_in(city)&#x27;])])</pre></div></div></div><div class=\"sk-parallel\"><div class=\"sk-parallel-item\"><div class=\"sk-item\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-12\" type=\"checkbox\" ><label for=\"sk-estimator-id-12\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">num</label><div class=\"sk-toggleable__content\"><pre>[&#x27;votes&#x27;, &#x27;approx_cost(for two people)&#x27;, &#x27;online_order_encoded&#x27;, &#x27;book_table_encoded&#x27;]</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-13\" type=\"checkbox\" ><label for=\"sk-estimator-id-13\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">SimpleImputer</label><div class=\"sk-toggleable__content\"><pre>SimpleImputer()</pre></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-14\" type=\"checkbox\" ><label for=\"sk-estimator-id-14\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">StandardScaler</label><div class=\"sk-toggleable__content\"><pre>StandardScaler()</pre></div></div></div></div></div></div></div></div><div class=\"sk-parallel-item\"><div class=\"sk-item\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-15\" type=\"checkbox\" ><label for=\"sk-estimator-id-15\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">cat</label><div class=\"sk-toggleable__content\"><pre>[&#x27;location&#x27;, &#x27;rest_type&#x27;, &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;, &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;, &#x27;listed_in(type)&#x27;, &#x27;listed_in(city)&#x27;]</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-16\" type=\"checkbox\" ><label for=\"sk-estimator-id-16\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">SimpleImputer</label><div class=\"sk-toggleable__content\"><pre>SimpleImputer(strategy=&#x27;most_frequent&#x27;)</pre></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-17\" type=\"checkbox\" ><label for=\"sk-estimator-id-17\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">OneHotEncoder</label><div class=\"sk-toggleable__content\"><pre>OneHotEncoder(handle_unknown=&#x27;ignore&#x27;)</pre></div></div></div></div></div></div></div></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-18\" type=\"checkbox\" ><label for=\"sk-estimator-id-18\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">RandomForestClassifier</label><div class=\"sk-toggleable__content\"><pre>RandomForestClassifier()</pre></div></div></div></div></div></div></div>"
      ],
      "text/plain": [
       "Pipeline(steps=[('preprocessor',\n",
       "                 ColumnTransformer(transformers=[('num',\n",
       "                                                  Pipeline(steps=[('imputer',\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  ('scaler',\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  ['votes',\n",
       "                                                   'approx_cost(for two '\n",
       "                                                   'people)',\n",
       "                                                   'online_order_encoded',\n",
       "                                                   'book_table_encoded']),\n",
       "                                                 ('cat',\n",
       "                                                  Pipeline(steps=[('imputer',\n",
       "                                                                   SimpleImputer(strategy='most_frequent')),\n",
       "                                                                  ('encoder',\n",
       "                                                                   OneHotEncoder(handle_unknown='ignore'))]),\n",
       "                                                  ['location', 'rest_type',\n",
       "                                                   'dish_liked', 'cuisines',\n",
       "                                                   'reviews_list', 'menu_item',\n",
       "                                                   'listed_in(type)',\n",
       "                                                   'listed_in(city)'])])),\n",
       "                ('model', RandomForestClassifier())])"
      ]
     },
     "execution_count": 46,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "classifier_pipeline2.fit(X,y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:15:45.782411Z",
     "iopub.status.busy": "2024-09-25T09:15:45.782127Z",
     "iopub.status.idle": "2024-09-25T09:20:03.674965Z",
     "shell.execute_reply": "2024-09-25T09:20:03.674011Z",
     "shell.execute_reply.started": "2024-09-25T09:15:45.782381Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Best Parameters: {'model__max_depth': None, 'model__n_estimators': 50, 'preprocessor__cat__imputer__strategy': 'most_frequent', 'preprocessor__num__imputer__strategy': 'mean'}\n",
      "Best Score: 0.8907097835023293\n"
     ]
    }
   ],
   "source": [
    "param_grid2 = {\n",
    "    'preprocessor__num__imputer__strategy': ['mean', 'median'],  # only valid for numeric columns\n",
    "    'preprocessor__cat__imputer__strategy': ['most_frequent'],  # valid for categorical columns\n",
    "    'model__n_estimators': [10, 50, 100],  # hyperparameter for Random Forest Classifier\n",
    "    'model__max_depth': [None, 5, 10]  # hyperparameter for Random Forest Classifier\n",
    "}\n",
    "\n",
    "# Perform GridSearchCV\n",
    "grid_search2 = GridSearchCV(classifier_pipeline2, param_grid2, cv=5, scoring='accuracy')\n",
    "\n",
    "# Fit the grid search\n",
    "grid_search2.fit(X, y)\n",
    "\n",
    "# Output the best parameters and score\n",
    "print(\"Best Parameters:\", grid_search2.best_params_)\n",
    "print(\"Best Score:\", grid_search2.best_score_)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:20:03.676384Z",
     "iopub.status.busy": "2024-09-25T09:20:03.676084Z",
     "iopub.status.idle": "2024-09-25T09:20:38.798135Z",
     "shell.execute_reply": "2024-09-25T09:20:38.797245Z",
     "shell.execute_reply.started": "2024-09-25T09:20:03.676352Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.8868183063853111\n"
     ]
    }
   ],
   "source": [
    "scores2 = cross_val_score(grid_search2.best_estimator_, X, y, cv=5, scoring='accuracy')\n",
    "print(\"Accuracy:\", scores2.mean())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:20:38.799691Z",
     "iopub.status.busy": "2024-09-25T09:20:38.799380Z",
     "iopub.status.idle": "2024-09-25T09:20:49.557151Z",
     "shell.execute_reply": "2024-09-25T09:20:49.556139Z",
     "shell.execute_reply.started": "2024-09-25T09:20:38.799658Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 1.0\n",
      "Classification Report:\n",
      "               precision    recall  f1-score   support\n",
      "\n",
      "           0       1.00      1.00      1.00      3429\n",
      "           1       1.00      1.00      1.00     14816\n",
      "\n",
      "    accuracy                           1.00     18245\n",
      "   macro avg       1.00      1.00      1.00     18245\n",
      "weighted avg       1.00      1.00      1.00     18245\n",
      "\n",
      "Confusion Matrix:\n",
      " [[ 3429     0]\n",
      " [    0 14816]]\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "['best_pipeline_model2.pkl']"
      ]
     },
     "execution_count": 49,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "best_pipeline2 = grid_search2.best_estimator_\n",
    "best_pipeline2.fit(X, y)\n",
    "\n",
    "# Predict on the training data (or a separate test set)\n",
    "y_pred2 = best_pipeline2.predict(X)\n",
    "\n",
    "# Print evaluation metrics\n",
    "print(\"Accuracy:\", accuracy_score(y, y_pred2))\n",
    "print(\"Classification Report:\\n\", classification_report(y, y_pred2))\n",
    "print(\"Confusion Matrix:\\n\", confusion_matrix(y, y_pred2))\n",
    "\n",
    "# Save the best model for future use\n",
    "joblib.dump(best_pipeline2, 'best_pipeline_model2.pkl')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:53:20.352068Z",
     "iopub.status.busy": "2024-09-25T09:53:20.351575Z",
     "iopub.status.idle": "2024-09-25T09:53:20.648668Z",
     "shell.execute_reply": "2024-09-25T09:53:20.647691Z",
     "shell.execute_reply.started": "2024-09-25T09:53:20.352028Z"
    }
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-6 {color: black;background-color: white;}#sk-container-id-6 pre{padding: 0;}#sk-container-id-6 div.sk-toggleable {background-color: white;}#sk-container-id-6 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-6 label.sk-toggleable__label-arrow:before {content: \"▸\";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-6 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-6 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-6 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-6 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-6 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-6 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: \"▾\";}#sk-container-id-6 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-6 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-6 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-6 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-6 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-6 div.sk-parallel-item::after {content: \"\";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-6 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-6 div.sk-serial::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-6 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-6 div.sk-item {position: relative;z-index: 1;}#sk-container-id-6 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-6 div.sk-item::before, #sk-container-id-6 div.sk-parallel-item::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-6 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-6 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-6 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-6 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-6 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-6 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-6 div.sk-label-container {text-align: center;}#sk-container-id-6 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-6 div.sk-text-repr-fallback {display: none;}</style><div id=\"sk-container-id-6\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>Pipeline(steps=[(&#x27;preprocessor&#x27;,\n",
       "                 ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  (&#x27;scaler&#x27;,\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  [&#x27;votes&#x27;,\n",
       "                                                   &#x27;approx_cost(for two &#x27;\n",
       "                                                   &#x27;people)&#x27;,\n",
       "                                                   &#x27;online_order_encoded&#x27;,\n",
       "                                                   &#x27;book_table_encoded&#x27;]),\n",
       "                                                 (&#x27;cat&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                                  (&#x27;encoder&#x27;,\n",
       "                                                                   OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                                  [&#x27;location&#x27;, &#x27;rest_type&#x27;,\n",
       "                                                   &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;,\n",
       "                                                   &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                                   &#x27;listed_in(type)&#x27;,\n",
       "                                                   &#x27;listed_in(city)&#x27;])])),\n",
       "                (&#x27;model&#x27;, KNeighborsClassifier())])</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item sk-dashed-wrapped\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-46\" type=\"checkbox\" ><label for=\"sk-estimator-id-46\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">Pipeline</label><div class=\"sk-toggleable__content\"><pre>Pipeline(steps=[(&#x27;preprocessor&#x27;,\n",
       "                 ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  (&#x27;scaler&#x27;,\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  [&#x27;votes&#x27;,\n",
       "                                                   &#x27;approx_cost(for two &#x27;\n",
       "                                                   &#x27;people)&#x27;,\n",
       "                                                   &#x27;online_order_encoded&#x27;,\n",
       "                                                   &#x27;book_table_encoded&#x27;]),\n",
       "                                                 (&#x27;cat&#x27;,\n",
       "                                                  Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                                   SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                                  (&#x27;encoder&#x27;,\n",
       "                                                                   OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                                  [&#x27;location&#x27;, &#x27;rest_type&#x27;,\n",
       "                                                   &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;,\n",
       "                                                   &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                                   &#x27;listed_in(type)&#x27;,\n",
       "                                                   &#x27;listed_in(city)&#x27;])])),\n",
       "                (&#x27;model&#x27;, KNeighborsClassifier())])</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item sk-dashed-wrapped\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-47\" type=\"checkbox\" ><label for=\"sk-estimator-id-47\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">preprocessor: ColumnTransformer</label><div class=\"sk-toggleable__content\"><pre>ColumnTransformer(transformers=[(&#x27;num&#x27;,\n",
       "                                 Pipeline(steps=[(&#x27;imputer&#x27;, SimpleImputer()),\n",
       "                                                 (&#x27;scaler&#x27;, StandardScaler())]),\n",
       "                                 [&#x27;votes&#x27;, &#x27;approx_cost(for two people)&#x27;,\n",
       "                                  &#x27;online_order_encoded&#x27;,\n",
       "                                  &#x27;book_table_encoded&#x27;]),\n",
       "                                (&#x27;cat&#x27;,\n",
       "                                 Pipeline(steps=[(&#x27;imputer&#x27;,\n",
       "                                                  SimpleImputer(strategy=&#x27;most_frequent&#x27;)),\n",
       "                                                 (&#x27;encoder&#x27;,\n",
       "                                                  OneHotEncoder(handle_unknown=&#x27;ignore&#x27;))]),\n",
       "                                 [&#x27;location&#x27;, &#x27;rest_type&#x27;, &#x27;dish_liked&#x27;,\n",
       "                                  &#x27;cuisines&#x27;, &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;,\n",
       "                                  &#x27;listed_in(type)&#x27;, &#x27;listed_in(city)&#x27;])])</pre></div></div></div><div class=\"sk-parallel\"><div class=\"sk-parallel-item\"><div class=\"sk-item\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-48\" type=\"checkbox\" ><label for=\"sk-estimator-id-48\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">num</label><div class=\"sk-toggleable__content\"><pre>[&#x27;votes&#x27;, &#x27;approx_cost(for two people)&#x27;, &#x27;online_order_encoded&#x27;, &#x27;book_table_encoded&#x27;]</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-49\" type=\"checkbox\" ><label for=\"sk-estimator-id-49\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">SimpleImputer</label><div class=\"sk-toggleable__content\"><pre>SimpleImputer()</pre></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-50\" type=\"checkbox\" ><label for=\"sk-estimator-id-50\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">StandardScaler</label><div class=\"sk-toggleable__content\"><pre>StandardScaler()</pre></div></div></div></div></div></div></div></div><div class=\"sk-parallel-item\"><div class=\"sk-item\"><div class=\"sk-label-container\"><div class=\"sk-label sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-51\" type=\"checkbox\" ><label for=\"sk-estimator-id-51\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">cat</label><div class=\"sk-toggleable__content\"><pre>[&#x27;location&#x27;, &#x27;rest_type&#x27;, &#x27;dish_liked&#x27;, &#x27;cuisines&#x27;, &#x27;reviews_list&#x27;, &#x27;menu_item&#x27;, &#x27;listed_in(type)&#x27;, &#x27;listed_in(city)&#x27;]</pre></div></div></div><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-serial\"><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-52\" type=\"checkbox\" ><label for=\"sk-estimator-id-52\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">SimpleImputer</label><div class=\"sk-toggleable__content\"><pre>SimpleImputer(strategy=&#x27;most_frequent&#x27;)</pre></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-53\" type=\"checkbox\" ><label for=\"sk-estimator-id-53\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">OneHotEncoder</label><div class=\"sk-toggleable__content\"><pre>OneHotEncoder(handle_unknown=&#x27;ignore&#x27;)</pre></div></div></div></div></div></div></div></div></div></div><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-54\" type=\"checkbox\" ><label for=\"sk-estimator-id-54\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">KNeighborsClassifier</label><div class=\"sk-toggleable__content\"><pre>KNeighborsClassifier()</pre></div></div></div></div></div></div></div>"
      ],
      "text/plain": [
       "Pipeline(steps=[('preprocessor',\n",
       "                 ColumnTransformer(transformers=[('num',\n",
       "                                                  Pipeline(steps=[('imputer',\n",
       "                                                                   SimpleImputer()),\n",
       "                                                                  ('scaler',\n",
       "                                                                   StandardScaler())]),\n",
       "                                                  ['votes',\n",
       "                                                   'approx_cost(for two '\n",
       "                                                   'people)',\n",
       "                                                   'online_order_encoded',\n",
       "                                                   'book_table_encoded']),\n",
       "                                                 ('cat',\n",
       "                                                  Pipeline(steps=[('imputer',\n",
       "                                                                   SimpleImputer(strategy='most_frequent')),\n",
       "                                                                  ('encoder',\n",
       "                                                                   OneHotEncoder(handle_unknown='ignore'))]),\n",
       "                                                  ['location', 'rest_type',\n",
       "                                                   'dish_liked', 'cuisines',\n",
       "                                                   'reviews_list', 'menu_item',\n",
       "                                                   'listed_in(type)',\n",
       "                                                   'listed_in(city)'])])),\n",
       "                ('model', KNeighborsClassifier())])"
      ]
     },
     "execution_count": 58,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model_KNN5.fit(X,y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T09:56:36.016365Z",
     "iopub.status.busy": "2024-09-25T09:56:36.015622Z",
     "iopub.status.idle": "2024-09-25T09:59:38.256643Z",
     "shell.execute_reply": "2024-09-25T09:59:38.255699Z",
     "shell.execute_reply.started": "2024-09-25T09:56:36.016326Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Best Parameters: {'model__n_neighbors': 3, 'model__weights': 'distance'}\n",
      "Best Score: 0.9414634146341463\n",
      "Accuracy: 0.9414634146341463\n",
      "Accuracy: 1.0\n",
      "Classification Report:\n",
      "               precision    recall  f1-score   support\n",
      "\n",
      "           0       1.00      1.00      1.00      3429\n",
      "           1       1.00      1.00      1.00     14816\n",
      "\n",
      "    accuracy                           1.00     18245\n",
      "   macro avg       1.00      1.00      1.00     18245\n",
      "weighted avg       1.00      1.00      1.00     18245\n",
      "\n",
      "Confusion Matrix:\n",
      " [[ 3429     0]\n",
      " [    0 14816]]\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "['best_knn_model.pkl']"
      ]
     },
     "execution_count": 61,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "param_grid_knn = {\n",
    "    'model__n_neighbors': [3, 5, 7, 9, 11],  # number of nearest neighbors\n",
    "    'model__weights': ['uniform', 'distance'],  # weight function\n",
    "}\n",
    "\n",
    "# Perform GridSearchCV\n",
    "grid_search_knn = GridSearchCV(model_KNN5, param_grid_knn, cv=5, scoring='accuracy')\n",
    "\n",
    "# Fit the grid search\n",
    "grid_search_knn.fit(X, y)\n",
    "\n",
    "# Output the best parameters and score\n",
    "print(\"Best Parameters:\", grid_search_knn.best_params_)\n",
    "print(\"Best Score:\", grid_search_knn.best_score_)\n",
    "\n",
    "# Evaluate the best model using cross-validation\n",
    "scores_knn = cross_val_score(grid_search_knn.best_estimator_, X, y, cv=5, scoring='accuracy')\n",
    "print(\"Accuracy:\", scores_knn.mean())\n",
    "\n",
    "# Fit the best model to the entire dataset\n",
    "best_knn_pipeline = grid_search_knn.best_estimator_\n",
    "best_knn_pipeline.fit(X, y)\n",
    "\n",
    "# Predict on the training data (or a separate test set)\n",
    "y_pred_knn = best_knn_pipeline.predict(X)\n",
    "\n",
    "# Print evaluation metrics\n",
    "print(\"Accuracy:\", accuracy_score(y, y_pred_knn))\n",
    "print(\"Classification Report:\\n\", classification_report(y, y_pred_knn))\n",
    "print(\"Confusion Matrix:\\n\", confusion_matrix(y, y_pred_knn))\n",
    "\n",
    "# Save the best model for future use\n",
    "joblib.dump(best_knn_pipeline, 'best_knn_model.pkl')\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T10:10:55.410846Z",
     "iopub.status.busy": "2024-09-25T10:10:55.410415Z",
     "iopub.status.idle": "2024-09-25T10:10:55.629664Z",
     "shell.execute_reply": "2024-09-25T10:10:55.628735Z",
     "shell.execute_reply.started": "2024-09-25T10:10:55.410786Z"
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 640x480 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.heatmap(confusion_matrix(y, y_pred_knn), annot=True, cmap='Blues')\n",
    "plt.xlabel('Predicted labels')\n",
    "plt.ylabel('True labels')\n",
    "plt.title('Confusion Matrix')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 74,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T10:22:46.526666Z",
     "iopub.status.busy": "2024-09-25T10:22:46.525880Z",
     "iopub.status.idle": "2024-09-25T10:23:23.092152Z",
     "shell.execute_reply": "2024-09-25T10:23:23.091130Z",
     "shell.execute_reply.started": "2024-09-25T10:22:46.526628Z"
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "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SND06dO1a9cutWvXTjExMcrKyiq1fuvWrRo8eLBGjBihtLQ0xcbGKjY2Vnv37rXXfPPNN+revbtatGihTZs26auvvtLUqVPl6elZWbsFAABuclX6bfCRkZHq1KmT5s+fL+nKV1CEhIToscce04QJE0rUx8XFKS8vT2vXrrWPdenSRREREVq0aJEkadCgQXJzc9Py5ctvuK/c3Fz5+voqJyeH6wABAFBNOPP6XWVngAoLC7Vz505FR0f/2IyLi6Kjo5WamlrqOqmpqQ71khQTE2OvLy4u1gcffKBmzZopJiZGAQEBioyMVHJy8nV7uXjxonJzcx1uAADg1lVlASg7O1tFRUUKDAx0GA8MDFRGRkap62RkZFy3PisrSxcuXNBzzz2n3r1769///rceeOABDRgwQJ988sk1e0lKSpKvr6/9xveAAQBwa6vySdDlqbi4WJLUv39/PfHEE4qIiNCECRN0//33298iK83EiROVk5Njv504caKyWgYAAFWgyr4LzN/fX66ursrMzHQYz8zMVFBQUKnrBAUFXbfe399fNWrUUKtWrRxqWrZsqU8//fSavXh4eMjDw+NGdgMAAFRDVXYGyN3dXR06dFBKSop9rLi4WCkpKYqKiip1naioKId6SdqwYYO93t3dXZ06ddKhQ4ccav7zn/+oUaNG5bwHAACguqrSb4NPSEjQsGHD1LFjR3Xu3Fnz5s1TXl6e4uPjJUlDhw5Vw4YNlZSUJEkaO3asevbsqTlz5qhv375atWqVduzYocWLF9u3OX78eMXFxenOO+/U3XffrfXr1+v999/Xpk2bqmIXAQDATahKA1BcXJxOnz6tadOmKSMjQxEREVq/fr19ovPx48fl4vLjSaquXbtqxYoVmjJliiZNmqSwsDAlJyerTZs29poHHnhAixYtUlJSkh5//HE1b95c//jHP9S9e/dK3z8AAHBzqtLrAN2suA4QAADVT7W4DhAAAEBVIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLIQABAADLuSkC0IIFC9S4cWN5enoqMjJS27dvv279mjVr1KJFC3l6eio8PFzr1q1zWD58+HDZbDaHW+/evStyFwAAQDVS5QFo9erVSkhI0PTp07Vr1y61a9dOMTExysrKKrV+69atGjx4sEaMGKG0tDTFxsYqNjZWe/fudajr3bu3Tp06Zb+tXLmyMnYHAABUAzZjjKnKBiIjI9WpUyfNnz9fklRcXKyQkBA99thjmjBhQon6uLg45eXlae3atfaxLl26KCIiQosWLZJ05QzQuXPnlJycfEM95ebmytfXVzk5OfLx8bmhbQAAgMrlzOt3lZ4BKiws1M6dOxUdHW0fc3FxUXR0tFJTU0tdJzU11aFekmJiYkrUb9q0SQEBAWrevLlGjx6tM2fOlP8OAACAaqlGVT54dna2ioqKFBgY6DAeGBiogwcPlrpORkZGqfUZGRn2+71799aAAQMUGhqqb775RpMmTVKfPn2UmpoqV1fXEtu8ePGiLl68aL+fm5v7a3YLAADc5Ko0AFWUQYMG2X8ODw9X27Ztdfvtt2vTpk3q1atXifqkpCQlJiZWZosAAKAKVelbYP7+/nJ1dVVmZqbDeGZmpoKCgkpdJygoyKl6SWrSpIn8/f319ddfl7p84sSJysnJsd9OnDjh5J4AAIDqpEoDkLu7uzp06KCUlBT7WHFxsVJSUhQVFVXqOlFRUQ71krRhw4Zr1kvSyZMndebMGTVo0KDU5R4eHvLx8XG4AQCAW1eVfww+ISFBr7zyit544w0dOHBAo0ePVl5enuLj4yVJQ4cO1cSJE+31Y8eO1fr16zVnzhwdPHhQM2bM0I4dOzRmzBhJ0oULFzR+/Hh9/vnnOnr0qFJSUtS/f381bdpUMTExVbKPAADg5lLlc4Di4uJ0+vRpTZs2TRkZGYqIiND69evtE52PHz8uF5cfc1rXrl21YsUKTZkyRZMmTVJYWJiSk5PVpk0bSZKrq6u++uorvfHGGzp37pyCg4N177336tlnn5WHh0eV7CMAALi5VPl1gG5GXAcIAIDqp9pc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AACgSlTodYCufunpz+3evVt169Z1dnMAAACVrsxzgOrUqSObzSabzaZmzZo5hKCioiJduHBBo0aNqpAmAQAAylOZA9C8efNkjNEf//hHJSYmytfX177M3d1djRs3VlRUVIU0CQAAUJ7KHICGDRsmSQoNDVXXrl3l5uZWYU0BAABUJKc/Bt+zZ0/7zwUFBSosLHRYzqRhAABws3N6EnR+fr7GjBmjgIAAeXt7q06dOg43AACAm53TAWj8+PH6+OOPtXDhQnl4eOjVV19VYmKigoODtWzZsoroEQAAoFw5/RbY+++/r2XLlumuu+5SfHy8evTooaZNm6pRo0Z68803NWTIkIroEwAAoNw4fQbo7NmzatKkiaQr833Onj0rSerevbs2b95cvt0BAABUAKcDUJMmTZSeni5JatGihd566y1JV84M+fn5lWtzAAAAFcHpABQfH6/du3dLkiZMmKAFCxbI09NTTzzxhMaPH1/uDQIAAJQ3p78L7OeOHTumnTt3qmnTpmrbtm159VWl+C4wAACqH2dev52eBP1TBQUFatSokRo1avRrNgMAAFCpnH4LrKioSM8++6waNmyoWrVq6ciRI5KkqVOn6rXXXiv3BgEAAMqb0wFo5syZWrp0qWbPni13d3f7eJs2bfTqq6+Wa3MAAAAVwekAtGzZMi1evFhDhgyRq6urfbxdu3Y6ePBguTYHAABQEZwOQN9++62aNm1aYry4uFiXLl0ql6YAAAAqktMBqFWrVtqyZUuJ8bffflt33HFHuTQFAABQkZz+FNi0adM0bNgwffvttyouLtY777yjQ4cOadmyZVq7dm1F9AgAAFCunD4D1L9/f73//vv66KOP5O3trWnTpunAgQN6//339V//9V8V0SMAAEC5KnMAOnLkiK5eM7FHjx7asGGDsrKylJ+fr08//VT33nvvDTexYMECNW7cWJ6enoqMjNT27duvW79mzRq1aNFCnp6eCg8P17p16+zLLl26pKefflrh4eHy9vZWcHCwhg4dqu++++6G+wMAALeWMgegsLAwnT592n4/Li5OmZmZv7qB1atXKyEhQdOnT9euXbvUrl07xcTEKCsrq9T6rVu3avDgwRoxYoTS0tIUGxur2NhY7d27V5KUn5+vXbt2aerUqdq1a5f9Lbp+/fr96l4BAMCtocxfheHi4qKMjAwFBARIkmrX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v7++/vprSRyryjZmzBitXbtWGzdu1G9+8xv7eGX9zatOr3cEoErg7u6uDh06KCUlxT5WXFyslJQURUVFVWFn1nLhwgV98803atCggTp06CA3NzeHY3Lo0CEdP37cfkyioqK0Z88ehz/eGzZskI+Pj1q1amWv+ek2rtZwXG9caGiogoKCHJ7X3Nxcbdu2zeHYnDt3Tjt37rTXfPzxxyouLlZkZKS9ZvPmzbp06ZK9ZsOGDWrevLnq1Kljr+H4la+TJ0/qzJkzatCggSSOVWUxxmjMmDF699139fHHHys0NNRheWX9zatWr3dVPQvbKlatWmU8PDzM0qVLzf79+80jjzxi/Pz8HGbbo3w9+eSTZtOmTSY9Pd189tlnJjo62vj7+5usrCxjzJWPhN52223m448/Njt27DBRUVEmKirKvv7Vj4Tee++95ssvvzTr16839evXL/UjoePHjzcHDhwwCxYs4GPwZXD+/HmTlpZm0tLSjCQzd+5ck5aWZo4dO2aMufIxeD8/P/Pee++Zr776yvTv37/Uj8HfcccdZtu2bebTTz81YWFhDh+tPnfunAkMDDQPPfSQ2bt3r1m1apWpWbNmiY9W16hRw/ztb38zBw4cMNOnT+ej1T9zvWN1/vx589RTT5nU1FSTnp5uPvroI9O+fXsTFhZmCgoK7NvgWFW80aNHG19fX7Np0yaHSxLk5+fbayrrb151eb0jAFWiF1980dx2223G3d3ddO7c2Xz++edV3dItLS4uzjRo0MC4u7ubhg0bmri4OPP111/bl//www/mT3/6k6lTp46pWbOmeeCBB8ypU6cctnH06FHTp08f4+XlZfz9/c2TTz5pLl265FCzceNGExERYdzd3U2TJk3MkiVLKmP3qrWNGzcaSSVuw4YNM8Zc+Sj81KlTTWBgoPHw8DC9evUyhw4dctjGmTNnzODBg02tWrWMj4+PiY+PN+fPn3eo2b17t+nevbvx8PAwDRs2NM8991yJXt566y3TrFkz4+7ublq3bm0++OCDCtvv6uh6xyo/P9/ce++9pn79+sbNzc00atTIPPzwwyVe6DhWFa+0YyTJ4e9RZf7Nqw6vdzZjjKnss04AAABViTlAAADAcghAAADAcghAAADAcghAAADAcghAAADAcghAAADAcghAAADAcghAAFDBbDabkpOTq7oNAD9BAAJwQ4YPHy6bzVbidvVLMH+tpUuXys/Pr1y2daOGDx+u2NjYKu0BQMWoUdUNAKi+evfurSVLljiM1a9fv4q6ubZLly7Jzc2tqtsAcBPhDBCAG+bh4aGgoCCHm6urqyTpvffeU/v27eXp6akmTZooMTFRly9ftq87d+5chYeHy9vbWyEhIfrTn/6kCxcuSJI2bdqk+Ph45eTk2M8szZgxQ1Lpbyf5+flp6dKlkqSjR4/KZrNp9erV6tmzpzw9PfXmm29Kkl599VW1bNlSnp6eatGihV566SWn9veuu+7S448/rj//+c+qW7eugoKC7H1ddfjwYd15553y9PRUq1attGHDhhLbOXHihAYOHCg/Pz/VrVtX/fv319GjRyVJBw8eVM2aNbVixQp7/VtvvSUvLy/t37/fqX4BXBsBCEC527Jli4YOHaqxY8dq//79evnll7V06VLNnDnTXuPi4qK///3v2rdvn9544w19/PHH+vOf/yxJ6tq1q+bNmycfHx+dOnVKp06d0lNPPeVUDxMmTNDYsWN14MABxcTE6M0339S0adM0c+ZMHThwQLNmzdLUqVP1xhtvOLXdN954Q97e3tq2bZtmz56tZ555xh5yiouLNWDAALm7u2vbtm1atGiRnn76aYf1L126pJiYGNWuXVtbtmzRZ599plq1aql3794qLCxUixYt9Le//U1/+tOfdPz4cZ08eVKjRo3S888/r1atWjnVK4DrqOpvYwVQPQ0bNsy4uroab29v++13v/udMcaYXr16mVmzZjnUL1++3DRo0OCa21uzZo2pV6+e/f6SJUuMr69viTpJ5t1333UY8/X1tX8jdXp6upFk5s2b51Bz++23mxUrVjiMPfvssyYqKuq6+9i/f3/7/Z49e5ru3bs71HTq1Mk8/fTTxhhj/vWvf5kaNWqYb7/91r78ww8/dOh5+fLlpnnz5qa4uNhec/HiRePl5WX+9a9/2cf69u1revToYXr16mXuvfdeh3oAvx5zgADcsLvvvlsLFy603/f29pYk7d69W5999pnDGZ+ioiIVFBQoPz9fNWvW1EcffaSkpCQdPHhQubm5unz5ssPyX6tjx472n/Py8vTNN99oxIgRevjhh+3jly9flq+vr1Pbbdu2rcP9Bg0aKCsrS5J04MABhYSEKDg42L48KirKoX737t36+uuvVbt2bYfxgoICffPNN/b7r7/+upo1ayYXFxft27dPNpvNqT4BXB8BCMAN8/b2VtOmTUuMX7hwQYmJiRowYECJZZ6enjp69Kjuv/9+jR49WjNnzlTdunX16aefasSIESosLLxuALLZbDLGOIxdunSp1N5+2o8kvfLKK4qMjHSouzpnqax+PpnaZrOpuLi4zOtfuHBBHTp0sM9L+qmfTiDfvXu38vLy5OLiolOnTqlBgwZO9Qng+ghAAMpd+/btdejQoVLDkSTt3LlTxcXFmjNnjlxcrkxFfOuttxxq3N3dVVRUVGLd+vXr69SpU/b7hw8fVn5+/nX7CQwMVHBwsI4cOaIhQ4Y4uztl1rJlS504ccIhsHz++ecONe3bt9fq1asVEBAgHx+fUrdz9uxZDR8+XJMnT9apU6c0ZMgQ7dq1S15eXhXWO2A1TIIGUO6mTZumZcuWKTExUfv27dOBAwe0atUqTZkyRZLUtGlTXbp0SS+++KKOHDmi5cuXa9GiRQ7baNy4sS5cuKCUlBRlZ2fbQ84999yj+fPnKy0tTTt27NCoUaPK9BH3xMREJSUl6e9//7v+85//aM+ePVqyZInmzp1bbvsdHR2tZs2aadiwYdq9e7e2bNmiyZMnO9QMGTJE/v7+6t+/v7Zs2aL09HRt2rRJjz/+uE6ePClJGjVqlEJCQjRlyhTNnTtXRUVFTk8CB3B9BCAA5S4mJkZr167Vv//9b3Xq1EldunTR//7v/6pRo0aSpHbt2mnu3Ll6/vnn1aZNG7355ptKSkpy2EbXrl01atQoxcXFqX79+po9e7Ykac6cOQoJCVGPHj30+9//Xk899VSZ5gyNHDlSr776qpYsWaLw8HD17NlTS5cuVWhoaLntt4uLi95991398MMP6ty5s0aOHOkwD0qSatasqc2bN+u2227TgAED1LJlS40YMUIFBQXy8fHRsmXLtG7dOi1fvlw1atSQt7e3/u///k+vvPKKPvzww3LrFbA6m/n5m+kAAAC3OM4AAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAyyEAAQAAy/l/NhlEUUh7fpEAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "\n",
    "feature_importances = best_pipeline2.steps[1][1].feature_importances_\n",
    "plt.bar(range(len(feature_importances)), feature_importances)\n",
    "plt.xlabel('Feature Index')\n",
    "plt.ylabel('Feature Importance')\n",
    "plt.title('Feature Importance')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 75,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T10:23:39.113229Z",
     "iopub.status.busy": "2024-09-25T10:23:39.112529Z",
     "iopub.status.idle": "2024-09-25T10:25:15.436953Z",
     "shell.execute_reply": "2024-09-25T10:25:15.435880Z",
     "shell.execute_reply.started": "2024-09-25T10:23:39.113188Z"
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "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OdVRGgIwYcKEFn28iIiIiIh0bi3qrG643Gx9/4UGT5jsWPWGkxGAeEs+WkREREREugBHiUgwGATDJB4NJ58betH1FJ1wkaOdskxXIjmp3wpYREREREQOLo4WIrt27YJ4LPnYsDyUPHMXpe88RTxuL+EwLC/D59ztbJYiIiIiItKl2L41y+/3c+FFF6U8N/DU2URqKjAw2bTkKYpOnkk8GsKTW0gsEqJbv6EYhkntzi14e/UjuDvRlT1Suat1z0JERERERDoV2wuR4uJigrW1ycem28tXr83b+wbDpHTxE/Y/2TDJzc21/34REREREekybN2a5ff7uSgtDel//HnJXbIOu/B6Ck+4yFkPEcti9OjRDqYqIiIiIiJdha1EJBAIUNsgDXG5vfjffirxwDDZMP8uhx9rMPe+e9VDRERERETkIGUrESktLU15PPTk8zHqe4jEY+QfcZLDjupudVQXERERETmIGfFmtrvy+/0MGz6CUDCRiLjcXqLhYIMRzJSdtGx8JPPmPcCcOXNaMl8REREREekCmk1EAoFAchECcPiUGXvTEKDg6ClKQ0RERERExBFHndU9Xi/FrzXYGcswCXz0poMRVBsiIiIiIiIOGxrO/MY3cFl71y69lYaIiIiIiEgL2E5EXJabhx56aO8ThskOpSEiIiIiItICzSYiBQUF+LKyiUbCyeeGXnw9RU77higNERERERGROs3umgWwdOlSTp58CpFwqAW7ZIF2yhIRERERkYZs1Yh4vd7EIgQgHqPw2HPAZb/OXWmIiIiIiIg05GjXLADT7WXrBy86OEK1ISIiIiIiksrRrlkA/Sed5ygN8Xg9SkNERERERCSFo4WI4XLjX/wURCPNvtdlJoZeMH++0hAREREREUlhayFSv3NWPBrGsDlwNBYjO8vH6NGj92N6IiIiIiLSFdnaNQvA7/cTCAQoLS2lrKxsn+/Nzc2lqKiIgoICpSEiIiIiItKI7YWIiIiIiIhIa3FcrC4iIiIiIrK/tBAREREREZE2p4WIiIiIiIi0OS1ERERERESkzWkhIiIiIiIibU4LERERERERaXP/H5sjoh0oBNwDAAAAAElFTkSuQmCC",
      "text/plain": [
       "<Figure size 1000x800 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "from sklearn.tree import plot_tree\n",
    "\n",
    "plt.figure(figsize=(10, 8))\n",
    "plot_tree(best_pipeline2.steps[1][1].estimators_[0], filled=True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 78,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T10:26:26.236067Z",
     "iopub.status.busy": "2024-09-25T10:26:26.235682Z",
     "iopub.status.idle": "2024-09-25T10:26:55.852590Z",
     "shell.execute_reply": "2024-09-25T10:26:55.851590Z",
     "shell.execute_reply.started": "2024-09-25T10:26:26.236031Z"
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAjUAAAHHCAYAAABHp6kXAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/xnp5ZAAAACXBIWXMAAA9hAAAPYQGoP6dpAAAz0klEQVR4nO3deXxTVf7/8XcKbVoKbUFKW6S0UGR3YbMiIiBIUXRg3EAZpQiMKCh+wY1BQfSrRXQQBxFFR7ZRcUVHUGZYFRVRQVFWAUEQKaDYDWgp7fn94Y98DS0lTdMmOX09H488aM499+Zzc5N739ycmziMMUYAAABBLsTfBQAAAPgCoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBkBAWbJkiS644AKFh4fL4XAoKytLkjR//ny1bNlSoaGhiomJkSR1795d3bt3L/djOBwOPfzwwz6rGUBgINQAKNXOnTt12223qWnTpgoPD1dUVJS6dOmiZ555RseOHauUx/z11191ww03KCIiQjNmzND8+fMVGRmprVu3Kj09XSkpKXrxxRc1a9asSnl8X3r11Vc1bdo0f5cBVCsOfvsJwKkWL16s66+/Xk6nU7fccovatm2r48eP65NPPtHbb7+t9PT0SgkWS5Ys0RVXXKGlS5eqV69ervbnn39et99+u7Zv365mzZq52o8fPy5JCgsLK9fj5Ofnq2bNmqpZs6ZvCi/FVVddpY0bN2r37t2V9hgA3FXeOxpAUNq1a5cGDhyopKQkrVixQgkJCa5pI0eO1I4dO7R48eJKeeyDBw9KkuvjpTO1lzfMnBQeHu7VfAACGx8/AXAzZcoU5eXl6Z///KdboDmpWbNmGj16tCTpxIkTevTRR5WSkiKn06nk5GT97W9/U0FBQYn5PvzwQ3Xt2lWRkZGqU6eO+vbtq02bNrmmd+/eXYMHD5YkderUSQ6HQ+np6UpOTtbEiRMlSbGxsW7jYUobU5Ofn6+HH35YzZs3V3h4uBISEnTNNddo586drj6ljanZt2+fbr31VsXFxcnpdKpNmzZ6+eWX3fqsWrVKDodDb7zxhh577DE1atRI4eHh6tmzp3bs2OG2LosXL9aPP/4oh8Mhh8Oh5ORk1/Tp06erTZs2qlWrlurWrauOHTvq1VdfPc0WAeApztQAcPP++++radOmuvjii8/Yd9iwYZo7d66uu+46jR07VmvXrlVGRoa2bNmihQsXuvrNnz9fgwcPVlpamp544gkdPXpUM2fO1CWXXKKvv/5aycnJGj9+vFq0aKFZs2bpkUceUZMmTZSSkqL+/ftr3rx5WrhwoWbOnKnatWvrvPPOK7WeoqIiXXXVVVq+fLkGDhyo0aNHKzc3V0uXLtXGjRuVkpJS6nwHDhzQRRddJIfDoVGjRik2NlYffvihhg4dqpycHN19991u/SdPnqyQkBDdc889ys7O1pQpUzRo0CCtXbtWkjR+/HhlZ2frp59+0tNPPy1Jql27tiTpxRdf1F133aXrrrtOo0ePVn5+vr799lutXbtWN9100xmfcwBlMADw/2VnZxtJpl+/fmfs+8033xhJZtiwYW7t99xzj5FkVqxYYYwxJjc318TExJjhw4e79cvMzDTR0dFu7bNnzzaSzJdffunWd+LEiUaSOXTokFt7t27dTLdu3Vz3X375ZSPJTJ06tUS9xcXFrr8lmYkTJ7ruDx061CQkJJhffvnFbZ6BAwea6Ohoc/ToUWOMMStXrjSSTKtWrUxBQYGr3zPPPGMkme+++87V1rdvX5OUlFSijn79+pk2bdqUaAdQcXz8BMAlJydHklSnTp0z9v3ggw8kSWPGjHFrHzt2rCS5xt0sXbpUWVlZuvHGG/XLL7+4bjVq1FBqaqpWrlzps/rffvtt1a9fX3feeWeJaQ6Ho9R5jDF6++23dfXVV8sY41ZjWlqasrOztX79erd5hgwZ4jaep2vXrpKkH3744Yw1xsTE6KefftKXX35ZnlUD4AE+fgLgEhUVJUnKzc09Y98ff/xRISEhblcjSVJ8fLxiYmL0448/SpK2b98uSbrsssvKfExf2Llzp1q0aFGuq5oOHTqkrKwszZo167RXdJ0cqHxS48aN3e7XrVtXkvTbb7+d8fHuv/9+LVu2TBdeeKGaNWum3r1766abblKXLl08rhlA6Qg1AFyioqLUsGFDbdy40eN5TncG5KTi4mJJv4+riY+PLzG9Mi+r9sTJ+v7yl7+4Biqf6tQxPDVq1Ci1n/HgGzJatWqlbdu2adGiRVqyZInefvttPffcc5owYYImTZpUzuoB/BGhBoCbq666SrNmzdKaNWvUuXPn0/ZLSkpScXGxtm/frlatWrnaDxw4oKysLCUlJUmSa3BugwYN3L57pjKkpKRo7dq1KiwsVGhoqEfzxMbGqk6dOioqKvJpfWWFvcjISA0YMEADBgzQ8ePHdc011+ixxx7TuHHjuNwcqADG1ABwc9999ykyMlLDhg3TgQMHSkzfuXOnnnnmGV155ZWSVOJbc6dOnSpJ6tu3ryQpLS1NUVFRevzxx1VYWFhieYcOHfJZ7ddee61++eUXPfvssyWmne4sSo0aNXTttdfq7bffLvUMlbf1RUZGKjs7u0T7r7/+6nY/LCxMrVu3ljGm1OcHgOc4UwPATUpKil599VUNGDBArVq1cvtG4c8++0xvvvmm0tPTNXr0aA0ePFizZs1SVlaWunXrpi+++EJz585V//791aNHD0m/f6Q1c+ZM3XzzzWrfvr0GDhyo2NhY7dmzR4sXL1aXLl1KDSHeuOWWWzRv3jyNGTNGX3zxhbp27aojR45o2bJluuOOO9SvX79S55s8ebJWrlyp1NRUDR8+XK1bt9bhw4e1fv16LVu2TIcPHy53LR06dNDrr7+uMWPGqFOnTqpdu7auvvpq9e7dW/Hx8erSpYvi4uK0ZcsWPfvss+rbt69HA7QBlMGv114BCFjff/+9GT58uElOTjZhYWGmTp06pkuXLmb69OkmPz/fGGNMYWGhmTRpkmnSpIkJDQ01iYmJZty4ca7pf7Ry5UqTlpZmoqOjTXh4uElJSTHp6enmq6++cvWp6CXdxhhz9OhRM378eFdN8fHx5rrrrjM7d+509dEpl3QbY8yBAwfMyJEjTWJiomu+nj17mlmzZrmtgyTz5ptvus27a9cuI8nMnj3b1ZaXl2duuukmExMTYyS5Lu9+4YUXzKWXXmrOOuss43Q6TUpKirn33ntNdnZ26RsCgMf47ScAAGAFxtQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFihWn35XnFxsX7++WfVqVPnjL9XAwAAAoMxRrm5uWrYsKFCQk5/PqZahZqff/5ZiYmJ/i4DAAB4Ye/evWrUqNFpp1erUHPyK8j37t2rqKgoP1cDAAA8kZOTo8TExDP+lEi1CjUnP3KKiooi1AAAEGTONHSEgcIAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABghaANNZMnT5bD4dDdd9/t71IAAEAACMpQ8+WXX+qFF17Qeeed5+9SAABAgAi6UJOXl6dBgwbpxRdfVN26df1dDgAACBBBF2pGjhypvn37qlevXmfsW1BQoJycHLcbAACwU01/F1AeCxYs0Pr16/Xll1961D8jI0OTJk2q5KoAAEAgCJozNXv37tXo0aP1yiuvKDw83KN5xo0bp+zsbNdt7969lVwlAADwF4cxxvi7CE+8++67+vOf/6waNWq42oqKiuRwOBQSEqKCggK3aaXJyclRdHS0srOzFRUVVdklAwAAH/D0+B00Hz/17NlT3333nVvbkCFD1LJlS91///1nDDQAAMBuQRNq6tSpo7Zt27q1RUZG6qyzzirRDgAAqp+gGVMDAABQlqA5U1OaVatW+bsEAAAQIDhTA/hB8gOL/V0CAFiHUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABgBUINAACwAqEGAABYgVADAACsQKgBAABWINQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBq4LXkBxb7uwQAAFwINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABghaAJNRkZGerUqZPq1KmjBg0aqH///tq2bZu/ywIAAAEiaELNRx99pJEjR+rzzz/X0qVLVVhYqN69e+vIkSP+Lg0AAASAmv4uwFNLlixxuz9nzhw1aNBA69at06WXXuqnqgAAQKAImlBzquzsbElSvXr1TtunoKBABQUFrvs5OTmVXhcAAPCPoPn46Y+Ki4t19913q0uXLmrbtu1p+2VkZCg6Otp1S0xMrMIqcarkBxb7uwQAgMWCMtSMHDlSGzdu1IIFC8rsN27cOGVnZ7tue/furaIKAQBAVQu6j59GjRqlRYsW6eOPP1ajRo3K7Ot0OuV0OquoMgAA4E9BE2qMMbrzzju1cOFCrVq1Sk2aNPF3SQAAIIAETagZOXKkXn31Vb333nuqU6eOMjMzJUnR0dGKiIjwc3UAAMDfgmZMzcyZM5Wdna3u3bsrISHBdXv99df9XRoAAAgAQXOmxhjj7xIAAEAAC5ozNQAAAGUh1AAAACsQahBwguVL+oKlTgCoLgg1AADACoQaAABgBUINAACwAqEG1RrjYgDAHoQaAABgBUINAACwAqEGAABYgVADAACsQKixBANeAQDVHaEGAABYgVADAF7iDCkQWAg1AADACoQaAABgBUINAACwAqEGACzFmB9UN4QaAABgBUKNj/A/IgAA/ItQAwAArECoAQAAViDUAAAAKxBqggRjdgAAKBuhBgAQMPgPHCqCUFNNVdcdh23rbdv6AEBFEGoAAIAVCDUAAMAKhJoAF+gfL/iqPl+vZ6A/bwAA3yPUBBAOxNUD2xmVgdcVQKgBAL8jkAC+QagJEDbv1GxeNwBA4CDU+EFlH+QJEcGN7QcEJt6bgY9Qg6DAzgSofnjfB55A3yaEGj/zxQsk0F9kwais55TnGwACE6HGIp4ebDkow0a8rgEQahBUTj1wcSADgIorz740kPe7hBo/qawXBR+boDritQ1AItQELE920hXdkfv7QODvx0fVYntXHM8hUDZCDVyq81meQFm/QKkDOClQX5OBWpcv2LxulY1QY7lgeHMESo2BUgcAVDZb93eEmipk64voj6rDOgIAAhOhppo7GUIqEkZsCjKBfHVVINWCysN2BrxHqAkwgbhD80XwCUa+XN9gH9RtK39dxlpd31PwHq8VzxBqUKbTvZHO9AarjDdgsL2pg61eTwXTegVTrYGO57Jy8fz6BqEGPsObElWhKl9nyQ8s5gdoSxGMNQcbnmPvEGqqAC/O/8Nz8X+q6rngo46qwfN7ZtU5IFZ1bYH8XFSmoAs1M2bMUHJyssLDw5WamqovvvjC3yWVydcvrOr6Qg0WbB93PB/uvH0+gv07pKqixj8+RlX/ULC/t4G/Hz+QBFWoef311zVmzBhNnDhR69ev1/nnn6+0tDQdPHjQ36VJ8v2bqqxlVYcXcVWc+q8KNqyDP/jjp0Sqi0C+yq+8KiMoVlRZz28wP9fBIKhCzdSpUzV8+HANGTJErVu31vPPP69atWrp5Zdf9ndpAS0Y30S+qpkzZb8L1rpPp6JnLvxxZZuvX9PlXZ5trwFveBvmgvk/lmXV7ovXbqA9D0ETao4fP65169apV69erraQkBD16tVLa9asKXWegoIC5eTkuN2qEpfxll9FTvkG0+niyhAMZ7Y8rbEq/vd9up19oD+HfxQowSaYz0RU1nNYVWeCTv3blwHsj8sLmu1qgsS+ffuMJPPZZ5+5td97773mwgsvLHWeiRMnGkklbtnZ2ZVaa9L9iyp1+d4oT01VWb83j3XqPEn3L3JrO90yy9t+uuWfOs/J6SfbPKnldMvxdL6y+pRW75ke99Tay/P4nv7r6fLO1OapQHwf/lEg1+fNe+V0r7vKXE9f7dd88Tor7+vdm8ctax/hyXN/pu1akdo92e9URHZ2tkfH76A5U+ONcePGKTs723Xbu3evv0sCAACVpKa/C/BU/fr1VaNGDR04cMCt/cCBA4qPjy91HqfTKafTWRXlAQAAPwuaMzVhYWHq0KGDli9f7morLi7W8uXL1blzZz9WBki7J/f1dwkA4FeBsB8MmjM1kjRmzBgNHjxYHTt21IUXXqhp06bpyJEjGjJkiL9LA0oVCG9yAIGJ/YPvBVWoGTBggA4dOqQJEyYoMzNTF1xwgZYsWaK4uDh/lwbgFOywgxfbDsEqqEKNJI0aNUqjRo3ydxkAAJQQSIEwkGqpKkEzpgawXXXcAQFVhfeXb5+DQH0+CTWAjwTqmxwAyuKLfVeg7P+8CjWPPPKIjh49WqL92LFjeuSRRypcFAAg+ATKga06OPW5timYVIRXoWbSpEnKy8sr0X706FFNmjSpwkUBgO1sOIDg/7A9A4NXocYYI4fDUaJ9w4YNqlevXoWLAgAAKK9yXf1Ut25dORwOORwONW/e3C3YFBUVKS8vTyNGjPB5kcGGxA4AQNUrV6iZNm2ajDG69dZbNWnSJEVHR7umhYWFKTk5mW/3BQAAflGuUDN48GBJUpMmTXTxxRcrNDS0UooCqgvO6sF2vMZRlbz68r1u3bqpuLhY33//vQ4ePKji4mK36ZdeeqlPigMCwe7JfZX8wGJ/lwEAOAOvQs3nn3+um266ST/++KOMMW7THA6HioqKfFIcgPIjhAGorrwKNSNGjFDHjh21ePFiJSQklHolFIDgxUcGAIKRV6Fm+/bteuutt9SsWTNf1wMAAOAVr76nJjU1VTt27PB1LQAABJWqPKvJGdQz8+pMzZ133qmxY8cqMzNT5557bomroM477zyfFAcAAOApr0LNtddeK0m69dZbXW0Oh8P1TcMMFAaCh68HFlfGb9L4og4A9vMq1OzatcvXdQBBxdYDpq3rBaB68CrUJCUl+boOAACACvFqoLAkzZ8/X126dFHDhg31448/Svr9ZxTee+89nxUH4PQ4qwL4Bu8le3gVambOnKkxY8boyiuvVFZWlmsMTUxMjKZNm+bL+oBKxw4NAOzgVaiZPn26XnzxRY0fP141atRwtXfs2FHfffedz4oDUDkIcgBs5FWo2bVrl9q1a1ei3el06siRIxUuCqgMHMgBwG5ehZomTZrom2++KdG+ZMkStWrVqqI1AQAAlJtXVz+NGTNGI0eOVH5+vowx+uKLL/Taa68pIyNDL730kq9rBPyOszwAEPi8CjXDhg1TRESEHnzwQR09elQ33XSTGjZsqGeeeUYDBw70dY0AAhiBD0Cg8CrUSNKgQYM0aNAgHT16VHl5eWrQoIEv64IfBftBKtjrBwB4x+tQc1KtWrVUq1YtX9QCoBojjAKoKI9DTfv27bV8+XLVrVtX7dq1k8PhOG3f9evX+6Q4AAAAT3kcavr16yen0ylJ6t+/f2XVAyBIcGYFQKDxONRMnDix1L8BAAACgVffU/Pll19q7dq1JdrXrl2rr776qsJFAYDE2SAA5eNVqBk5cqT27t1bon3fvn0aOXJkhYsCAAAoL69CzebNm9W+ffsS7e3atdPmzZsrXBQAAEB5eRVqnE6nDhw4UKJ9//79qlmzwleJAwAAlJtXoaZ3794aN26csrOzXW1ZWVn629/+pssvv9xnxQEAAHjKq9MqTz31lC699FIlJSW5fq37m2++UVxcnObPn+/TAoFgw+BW2IrXNgKdV6Hm7LPP1rfffqtXXnlFGzZsUEREhIYMGaIbb7xRoaGhvq4RAADgjLweABMZGam//vWvvqwFAADAax6Hmn//+9+64oorFBoaqn//+99l9v3Tn/5U4cIAAADKw+NQ079/f2VmZqpBgwZl/kyCw+FQUVGRL2oDAADwmMehpri4uNS/AQQeBnQCqI48vqS7Xr16+uWXXyRJt956q3JzcyutKCCYECAAIDB4HGqOHz+unJwcSdLcuXOVn59faUUB1R1BCQDKz+OPnzp37qz+/furQ4cOMsborrvuUkRERKl9X375ZZ8VCAAA4AmPQ82//vUvPf3009q5c6ckKTs7m7M1AAC/4YwmTuVxqImLi9PkyZMlSU2aNNH8+fN11llnVVphAAAA5eHVQOEePXooLCys0ooCEHz4XzMAf2OgMAAAsEJQDBTevXu3Hn30Ua1YsUKZmZlq2LCh/vKXv2j8+PGcMQIAAJK8HCjscDiqdKDw1q1bVVxcrBdeeEHNmjXTxo0bNXz4cB05ckRPPfVUldQAAAACW1AMFO7Tp4/69Onjut+0aVNt27ZNM2fOJNQAAABJXv5K965du1x/5+fnKzw83GcFeSo7O1v16tUrs09BQYEKCgpc90+OCQIAAPbxeKDwHxUXF+vRRx/V2Wefrdq1a+uHH36QJD300EP65z//6dMCS7Njxw5Nnz5dt912W5n9MjIyFB0d7bolJiZWem0AAMA/vAo1//u//6s5c+ZoypQpbgN127Ztq5deesnj5TzwwANyOBxl3rZu3eo2z759+9SnTx9df/31Gj58eJnLHzdunLKzs123vXv3lm9FAQBA0PDq46d58+Zp1qxZ6tmzp0aMGOFqP//880uEkLKMHTtW6enpZfZp2rSp6++ff/5ZPXr00MUXX6xZs2adcflOp1NOp9PjehAc+D4UAEBpvAo1+/btU7NmzUq0FxcXq7Cw0OPlxMbGKjY21uPH7NGjhzp06KDZs2crJMSrk0wAAMBSXiWD1q1ba/Xq1SXa33rrLbVr167CRZ1q37596t69uxo3bqynnnpKhw4dUmZmpjIzM33+WAAAIDh5daZmwoQJGjx4sPbt26fi4mK988472rZtm+bNm6dFixb5ukYtXbpUO3bs0I4dO9SoUSO3acYYnz8eqg4fJQF24L2MQODVmZp+/frp/fff17JlyxQZGakJEyZoy5Ytev/993X55Zf7ukalp6fLGFPqDQAAQPLyTI0kde3aVUuXLvVlLQAAAF7zOtRI0rp167RlyxZJUps2bSplPA2AysdHBwBs4FWoOXjwoAYOHKhVq1YpJiZGkpSVlaUePXpowYIFHl/RBAAA4Ctejam58847lZubq02bNunw4cM6fPiwNm7cqJycHN11112+rhE+wP/EAQC28+pMzZIlS7Rs2TK1atXK1da6dWvNmDFDvXv39llxAAAAnvL6t59CQ0NLtIeGhqq4uLjCRQEAAJSXV6Hmsssu0+jRo/Xzzz+72vbt26f/+Z//Uc+ePX1WHAAAgKe8CjXPPvuscnJylJycrJSUFKWkpKhJkybKycnR9OnTfV0jAADAGXk1piYxMVHr16/XsmXLXD9g2apVK/Xq1cunxQEAAHiqXGdqVqxYodatWysnJ0cOh0OXX3657rzzTt15553q1KmT2rRpU+pvQgGViSu7AABSOUPNtGnTNHz4cEVFRZWYFh0drdtuu01Tp071WXEAAACeKleo2bBhg/r06XPa6b1799a6desqXBQAAEB5lSvUHDhwoNRLuU+qWbOmDh06VOGiAAAAyqtcoebss8/Wxo0bTzv922+/VUJCQoWLAgAAKK9yhZorr7xSDz30kPLz80tMO3bsmCZOnKirrrrKZ8UBAAB4qlyXdD/44IN655131Lx5c40aNUotWrSQJG3dulUzZsxQUVGRxo8fXymFAgAAlKVcoSYuLk6fffaZbr/9do0bN07GGEmSw+FQWlqaZsyYobi4uEopFAAAoCzl/vK9pKQkffDBB/rtt9+0Y8cOGWN0zjnnqG7dupVRHwAAgEcc5uTplmogJydH0dHRys7OLvW7dgAAQODx9Pjt1W8/AQAABBpCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABgBUINAACwAqEGAABYgVADAACsQKgBAABWINQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArBB0oaagoEAXXHCBHA6HvvnmG3+XAwAAAkTQhZr77rtPDRs29HcZAAAgwARVqPnwww/13//+V0899ZS/SwEAAAGmpr8L8NSBAwc0fPhwvfvuu6pVq5a/ywEAAAEmKEKNMUbp6ekaMWKEOnbsqN27d3s0X0FBgQoKClz3c3JyKqlCAADgb379+OmBBx6Qw+Eo87Z161ZNnz5dubm5GjduXLmWn5GRoejoaNctMTGxktYEAAD4m8MYY/z14IcOHdKvv/5aZp+mTZvqhhtu0Pvvvy+Hw+FqLyoqUo0aNTRo0CDNnTu31HlLO1OTmJio7OxsRUVF+WYlAABApcrJyVF0dPQZj99+DTWe2rNnj9tHRz///LPS0tL01ltvKTU1VY0aNfJoOZ4+KQAAIHB4evwOijE1jRs3drtfu3ZtSVJKSorHgQYAANgtqC7pBgAAOJ2gOFNzquTkZAXBp2YAAKAKcaYGAABYgVADAACsQKgBAABWINQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABgBUINAACwAqEGAABYgVADAACsQKgBAABWINQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABghaAKNYsXL1ZqaqoiIiJUt25d9e/f398lAQCAAFHT3wV46u2339bw4cP1+OOP67LLLtOJEye0ceNGf5cFAAACRFCEmhMnTmj06NF68sknNXToUFd769at/VgVAAAIJEHx8dP69eu1b98+hYSEqF27dkpISNAVV1zBmRoAAOASFKHmhx9+kCQ9/PDDevDBB7Vo0SLVrVtX3bt31+HDh087X0FBgXJyctxuAADATn4NNQ888IAcDkeZt61bt6q4uFiSNH78eF177bXq0KGDZs+eLYfDoTfffPO0y8/IyFB0dLTrlpiYWFWrBgAAqphfx9SMHTtW6enpZfZp2rSp9u/fL8l9DI3T6VTTpk21Z8+e0847btw4jRkzxnU/JyeHYAMAgKX8GmpiY2MVGxt7xn4dOnSQ0+nUtm3bdMkll0iSCgsLtXv3biUlJZ12PqfTKafT6bN6AQBA4AqKq5+ioqI0YsQITZw4UYmJiUpKStKTTz4pSbr++uv9XB0AAAgEQRFqJOnJJ59UzZo1dfPNN+vYsWNKTU3VihUrVLduXX+XBgAAAoDDGGP8XURVycnJUXR0tLKzsxUVFeXvcgAAgAc8PX4HxSXdAAAAZ0KoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABgBUINAACwAqEGAABYgVADAACsQKgBAABWINQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQAwAArECoAQAAViDUAAAAKxBqAACAFQg1AADACoQaAABgBUINAACwAqEGAABYgVADAACsQKgBAABWINQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACsQagAAgBUINQAAwAqEGgAAYAVCDQAAsEJNfxdQlYwxkqScnBw/VwIAADx18rh98jh+OtUq1OTm5kqSEhMT/VwJAAAor9zcXEVHR592usOcKfZYpLi4WD///LPq1Kkjh8Phs+Xm5OQoMTFRe/fuVVRUlM+WC99jWwUPtlXwYFsFh2DeTsYY5ebmqmHDhgoJOf3ImWp1piYkJESNGjWqtOVHRUUF3QulumJbBQ+2VfBgWwWHYN1OZZ2hOYmBwgAAwAqEGgAAYAVCjQ84nU5NnDhRTqfT36XgDNhWwYNtFTzYVsGhOmynajVQGAAA2IszNQAAwAqEGgAAYAVCDQAAsAKhBgAAWIFQ4wMzZsxQcnKywsPDlZqaqi+++MLfJVnt4YcflsPhcLu1bNnSNT0/P18jR47UWWedpdq1a+vaa6/VgQMH3JaxZ88e9e3bV7Vq1VKDBg1077336sSJE259Vq1apfbt28vpdKpZs2aaM2dOVaxeUPv444919dVXq2HDhnI4HHr33XfdphtjNGHCBCUkJCgiIkK9evXS9u3b3focPnxYgwYNUlRUlGJiYjR06FDl5eW59fn222/VtWtXhYeHKzExUVOmTClRy5tvvqmWLVsqPDxc5557rj744AOfr2+wOtN2Sk9PL/Ee69Onj1sftlPVyMjIUKdOnVSnTh01aNBA/fv317Zt29z6VOU+L+CPdwYVsmDBAhMWFmZefvlls2nTJjN8+HATExNjDhw44O/SrDVx4kTTpk0bs3//ftft0KFDrukjRowwiYmJZvny5earr74yF110kbn44otd00+cOGHatm1revXqZb7++mvzwQcfmPr165tx48a5+vzwww+mVq1aZsyYMWbz5s1m+vTppkaNGmbJkiVVuq7B5oMPPjDjx48377zzjpFkFi5c6DZ98uTJJjo62rz77rtmw4YN5k9/+pNp0qSJOXbsmKtPnz59zPnnn28+//xzs3r1atOsWTNz4403uqZnZ2ebuLg4M2jQILNx40bz2muvmYiICPPCCy+4+nz66aemRo0aZsqUKWbz5s3mwQcfNKGhoea7776r9OcgGJxpOw0ePNj06dPH7T12+PBhtz5sp6qRlpZmZs+ebTZu3Gi++eYbc+WVV5rGjRubvLw8V5+q2ucFw/GOUFNBF154oRk5cqTrflFRkWnYsKHJyMjwY1V2mzhxojn//PNLnZaVlWVCQ0PNm2++6WrbsmWLkWTWrFljjPl9hx4SEmIyMzNdfWbOnGmioqJMQUGBMcaY++67z7Rp08Zt2QMGDDBpaWk+Xht7nXqwLC4uNvHx8ebJJ590tWVlZRmn02lee+01Y4wxmzdvNpLMl19+6erz4YcfGofDYfbt22eMMea5554zdevWdW0rY4y5//77TYsWLVz3b7jhBtO3b1+3elJTU81tt93m03W0welCTb9+/U47D9vJfw4ePGgkmY8++sgYU7X7vGA43vHxUwUcP35c69atU69evVxtISEh6tWrl9asWePHyuy3fft2NWzYUE2bNtWgQYO0Z88eSdK6detUWFjotk1atmypxo0bu7bJmjVrdO655youLs7VJy0tTTk5Odq0aZOrzx+XcbIP29V7u3btUmZmptvzGh0drdTUVLdtExMTo44dO7r69OrVSyEhIVq7dq2rz6WXXqqwsDBXn7S0NG3btk2//fabqw/br2JWrVqlBg0aqEWLFrr99tv166+/uqaxnfwnOztbklSvXj1JVbfPC5bjHaGmAn755RcVFRW5vVAkKS4uTpmZmX6qyn6pqamaM2eOlixZopkzZ2rXrl3q2rWrcnNzlZmZqbCwMMXExLjN88dtkpmZWeo2OzmtrD45OTk6duxYJa2Z3U4+t2W9XzIzM9WgQQO36TVr1lS9evV8sv14X3qmT58+mjdvnpYvX64nnnhCH330ka644goVFRVJYjv5S3Fxse6++2516dJFbdu2laQq2+cFy/GuWv1KN+xwxRVXuP4+77zzlJqaqqSkJL3xxhuKiIjwY2WAHQYOHOj6+9xzz9V5552nlJQUrVq1Sj179vRjZdXbyJEjtXHjRn3yySf+LiVgcaamAurXr68aNWqUGGV+4MABxcfH+6mq6icmJkbNmzfXjh07FB8fr+PHjysrK8utzx+3SXx8fKnb7OS0svpERUURnLx08rkt6/0SHx+vgwcPuk0/ceKEDh8+7JPtx/vSO02bNlX9+vW1Y8cOSWwnfxg1apQWLVqklStXqlGjRq72qtrnBcvxjlBTAWFhYerQoYOWL1/uaisuLtby5cvVuXNnP1ZWveTl5Wnnzp1KSEhQhw4dFBoa6rZNtm3bpj179ri2SefOnfXdd9+57ZSXLl2qqKgotW7d2tXnj8s42Yft6r0mTZooPj7e7XnNycnR2rVr3bZNVlaW1q1b5+qzYsUKFRcXKzU11dXn448/VmFhoavP0qVL1aJFC9WtW9fVh+3nOz/99JN+/fVXJSQkSGI7VSVjjEaNGqWFCxdqxYoVatKkidv0qtrnBc3xzt8jlYPdggULjNPpNHPmzDGbN282f/3rX01MTIzbKHP41tixY82qVavMrl27zKeffmp69epl6tevbw4ePGiM+f3yxsaNG5sVK1aYr776ynTu3Nl07tzZNf/Jyxt79+5tvvnmG7NkyRITGxtb6uWN9957r9myZYuZMWMGl3R7IDc313z99dfm66+/NpLM1KlTzddff21+/PFHY8zvl3THxMSY9957z3z77bemX79+pV7S3a5dO7N27VrzySefmHPOOcftUuGsrCwTFxdnbr75ZrNx40azYMECU6tWrRKXCtesWdM89dRTZsuWLWbixIlcKvwHZW2n3Nxcc88995g1a9aYXbt2mWXLlpn27dubc845x+Tn57uWwXaqGrfffruJjo42q1atcrvE/ujRo64+VbXPC4bjHaHGB6ZPn24aN25swsLCzIUXXmg+//xzf5dktQEDBpiEhAQTFhZmzj77bDNgwACzY8cO1/Rjx46ZO+64w9StW9fUqlXL/PnPfzb79+93W8bu3bvNFVdcYSIiIkz9+vXN2LFjTWFhoVuflStXmgsuuMCEhYWZpk2bmtmzZ1fF6gW1lStXGkklboMHDzbG/H5Z90MPPWTi4uKM0+k0PXv2NNu2bXNbxq+//mpuvPFGU7t2bRMVFWWGDBlicnNz3fps2LDBXHLJJcbpdJqzzz7bTJ48uUQtb7zxhmnevLkJCwszbdq0MYsXL6609Q42ZW2no0ePmt69e5vY2FgTGhpqkpKSzPDhw0scuNhOVaO07STJbX9Ulfu8QD/eOYwxpqrPDgEAAPgaY2oAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1ACAlxwOh959911/lwHg/yPUAHCTnp4uh8NR4nbyxwwras6cOYqJifHJsryVnp6u/v37+7UGAL5X098FAAg8ffr00ezZs93aYmNj/VTN6RUWFio0NNTfZQAIEJypAVCC0+lUfHy8261GjRqSpPfee0/t27dXeHi4mjZtqkmTJunEiROueadOnapzzz1XkZGRSkxM1B133KG8vDxJ0qpVqzRkyBBlZ2e7zgA9/PDDkkr/KCcmJkZz5syRJO3evVsOh0Ovv/66unXrpvDwcL3yyiuSpJdeekmtWrVSeHi4WrZsqeeee65c69u9e3fddddduu+++1SvXj3Fx8e76jpp+/btuvTSSxUeHq7WrVtr6dKlJZazd+9e3XDDDYqJiVG9evXUr18/7d69W5K0detW1apVS6+++qqr/xtvvKGIiAht3ry5XPUCKB2hBoDHVq9erVtuuUWjR4/W5s2b9cILL2jOnDl67LHHXH1CQkL0j3/8Q5s2bdLcuXO1YsUK3XfffZKkiy++WNOmTVNUVJT279+v/fv365577ilXDQ888IBGjx6tLVu2KC0tTa+88oomTJigxx57TFu2bNHjjz+uhx56SHPnzi3XcufOnavIyEitXbtWU6ZM0SOPPOIKLsXFxbrmmmsUFhamtWvX6vnnn9f999/vNn9hYaHS0tJUp04drV69Wp9++qlq166tPn366Pjx42rZsqWeeuop3XHHHdqzZ49++uknjRgxQk888YRat25drloBnIa/f1ETQGAZPHiwqVGjhomMjHTdrrvuOmOMMT179jSPP/64W//58+ebhISE0y7vzTffNGeddZbr/uzZs010dHSJfpLMwoUL3dqio6NdvxS8a9cuI8lMmzbNrU9KSop59dVX3doeffRR07lz5zLXsV+/fq773bp1M5dccolbn06dOpn777/fGGPMf/7zH1OzZk2zb98+1/QPP/zQreb58+ebFi1amOLiYlefgoICExERYf7zn/+42vr27Wu6du1qevbsaXr37u3WH0DFMKYGQAk9evTQzJkzXfcjIyMlSRs2bNCnn37qdmamqKhI+fn5Onr0qGrVqqVly5YpIyNDW7duVU5Ojk6cOOE2vaI6duzo+vvIkSPauXOnhg4dquHDh7vaT5w4oejo6HIt97zzznO7n5CQoIMHD0qStmzZosTERDVs2NA1vXPnzm79N2zYoB07dqhOnTpu7fn5+dq5c6fr/ssvv6zmzZsrJCREmzZtksPhKFedAE6PUAOghMjISDVr1qxEe15eniZNmqRrrrmmxLTw8HDt3r1bV111lW6//XY99thjqlevnj755BMNHTpUx48fLzPUOBwOGWPc2goLC0ut7Y/1SNKLL76o1NRUt34nxwB56tQBxw6HQ8XFxR7Pn5eXpw4dOrjG+fzRHwdZb9iwQUeOHFFISIj279+vhISEctUJ4PQINQA81r59e23btq3UwCNJ69atU3Fxsf7+978rJOT3IXtvvPGGW5+wsDAVFRWVmDc2Nlb79+933d++fbuOHj1aZj1xcXFq2LChfvjhBw0aNKi8q+OxVq1aae/evW4h5PPPP3fr0759e73++utq0KCBoqKiSl3O4cOHlZ6ervHjx2v//v0aNGiQ1q9fr4iIiEqrHahOGCgMwGMTJkzQvHnzNGnSJG3atElbtmzRggUL9OCDD0qSmjVrpsLCQk2fPl0//PCD5s+fr+eff95tGcnJycrLy9Py5cv1yy+/uILLZZddpmeffVZff/21vvrqK40YMcKjy7UnTZqkjIwM/eMf/9D333+v7777TrNnz9bUqVN9tt69evVS8+bNNXjwYG3YsEGrV6/W+PHj3foMGjRI9evXV79+/bR69Wrt2rVLq1at0l133aWffvpJkjRixAglJibqwQcf1NSpU1VUVFTugdIATo9QA8BjaWlpWrRokf773/+qU6dOuuiii/T0008rKSlJknT++edr6tSpeuKJJ9S2bVu98sorysjIcFvGxRdfrBEjRmjAgAGKjY3VlClTJEl///vflZiYqK5du+qmm27SPffc49EYnGHDhumll17S7Nmzde6556pbt26aM2eOmjRp4rP1DgkJ0cKFC3Xs2DFdeOGFGjZsmNu4IkmqVauWPv74YzVu3FjXXHONWrVqpaFDhyo/P19RUVGaN2+ePvjgA82fP181a9ZUZGSk/vWvf+nFF1/Uhx9+6LNagerMYU79EBsAACAIcaYGAABYgVADAACsQKgBAABWINQAAAArEGoAAIAVCDUAAMAKhBoAAGAFQg0AALACoQYAAFiBUAMAAKxAqAEAAFYg1AAAACv8P1BUgzr5qdH5AAAAAElFTkSuQmCC",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "\n",
    "coefficients = best_pipeline.steps[1][1].coef_[0]\n",
    "plt.bar(range(len(coefficients)), coefficients)\n",
    "plt.xlabel('Feature Index')\n",
    "plt.ylabel('Coefficient')\n",
    "plt.title('Coefficients')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 79,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T10:26:55.854622Z",
     "iopub.status.busy": "2024-09-25T10:26:55.854273Z",
     "iopub.status.idle": "2024-09-25T10:27:25.689862Z",
     "shell.execute_reply": "2024-09-25T10:27:25.688806Z",
     "shell.execute_reply.started": "2024-09-25T10:26:55.854586Z"
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "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vLjWCwQAAKiK10dkLr74Yv3www+69tprVVhYqMLCQg0aNEjbtm1T375966JGAACASnl9sq/VcLIvAADW4+n+26OvljZu3KhOnTopICBAGzdurLZv586dvasUAACghjwKMl27dlV+fr5atmyprl27ymazqbIDOTabTWVlZbVeJAAAQGU8CjI5OTmKiopy/Q0AAOAPPAoyrVq1cv39008/qU+fPgoMdJ/02LFj+uKLL9z6AgAA1CWvr1q65JJLKr3xXVFRkS655JJaKQoAAMATXgcZY4xsNluF9v3796tp06a1UhQAAIAnPL4h3qBBgyT9cULviBEjFBwc7BpXVlamjRs3qk+fPrVfIQAAQBU8DjIOh0PSH0dkmjdvrtDQUNe4oKAg9e7dW7fddlvtVwgAAFAFj4PM7NmzJUmtW7fWfffdx9dIAADA57izLwAA8Du1emffP1uwYIHeffdd5ebm6ujRo27jvvrqq5rMEgAAwGteX7U0ffp03XzzzYqOjtbXX3+tnj17KiIiQjt37lS/fv3qokYAAIBKeR1kZsyYoZdfflnPPfecgoKCdP/992v58uW6++67VVRUVONCnnjiCdlsNo0dO9bVVlxcrLS0NEVERKhZs2YaPHiwCgoKarwMAADQsHgdZHJzc12XWYeGhurgwYOSpJtuuklvv/12jYpYt26dXnrppQo/ODlu3Dh9+OGHmj9/vlatWqU9e/a4LgMHAADwOsjExMS47uybkJCgNWvWSPrjN5hqct7woUOHNGzYML3yyitq0aKFq72oqEizZs3StGnTdOmll6p79+6aPXu2vvjiC9cyAQDA6c3rIHPppZfqgw8+kCTdfPPNGjdunC6//HJdf/31uvbaa70uIC0tTf3791dKSopb+4YNG1RaWurWnpSUpISEBGVnZ1c5v5KSEjmdTrcBAAA0TF5ftfTyyy+rvLxcklznr3zxxRe65pprdMcdd3g1r3nz5umrr77SunXrKozLz89XUFCQwsLC3Nqjo6OVn59f5TwzMjI0ZcoUr+oAAADW5HWQCQgIUEDA/w7k3HDDDbrhhhskSbt379YZZ5zh0Xzy8vJ0zz33aPny5QoJCfG2jCpNmDBB6enprsdOp1Px8fG1Nn8AAOA/vP5qqTL5+fm666671L59e4+n2bBhg/bt26du3bopMDBQgYGBWrVqlaZPn67AwEBF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klRvn3lW2d9Z4icKgH79+rn+7ty5s3r16qVWrVrp3XffVWhoqA8rAxqGG264wfX3ueeeq86dO6tt27ZauXKlLrvsMh9WdnpLS0vTpk2btHr1al+X4rc4IuOlyMhINWrUqMLZ4QUFBYqJifFRVaefsLAwnXXWWfrxxx8VExOjo0ePqrCw0K3PidskJiam0m12fFx1fex2O2Gpho4/t9W9X2JiYrRv3z638ceOHdOBAwdqZfvxvqyZNm3aKDIyUj/++KMktpMvjBkzRh999JE++eQTnXnmma72+vrMs8r+jiDjpaCgIHXv3l1ZWVmutvLycmVlZSk5OdmHlZ1eDh06pB07dig2Nlbdu3dX48aN3bbJtm3blJub69omycnJ+u6779w+iJcvXy673a6OHTu6+pw4j+N92K41l5iYqJiYGLfn1el0au3atW7bprCwUBs2bHD1WbFihcrLy9WrVy9Xn08//VSlpaWuPsuXL9fZZ5+tFi1auPqw/WrPzz//rP379ys2NlYS26k+GWM0ZswYLVy4UCtWrFBiYqLb+Pr6zLPM/s7XZxtb0bx580xwcLDJzMw0W7ZsMbfffrsJCwtzOzsctevee+81K1euNDk5Oebzzz83KSkpJjIy0uzbt88Y88eliAkJCWbFihVm/fr1Jjk52SQnJ7umP34p4hVXXGG++eYbs3TpUhMVFVXppYjjx483W7duNS+88AKXX3vg4MGD5uuvvzZff/21kWSmTZtmvv76a/PTTz8ZY/64/DosLMy8//77ZuPGjWbAgAGVXn593nnnmbVr15rVq1eb9u3bu13WW1hYaKKjo81NN91kNm3aZObNm2eaNGlS4bLewMBA8+9//9ts3brVTJo0ict6T1Dddjp48KC57777THZ2tsnJyTEff/yx6datm2nfvr0pLi52zYPtVD/uvPNO43A4zMqVK90uhz9y5IirT3195llhf0eQqaHnnnvOJCQkmKCgINOzZ0+zZs0aX5fUoF1//fUmNjbWBAUFmTPOOMNcf/315scff3SN//33383o0aNNixYtTJMmTcy1115r9u7d6zaPXbt2mX79+pnQ0FATGRlp7r33XlNaWurW55NPPjFdu3Y1QUFBpk2bNmb27Nn1sXqW9sknnxhJFYbhw4cbY/64BPvhhx820dHRJjg42Fx22WVm27ZtbvPYv3+/GTp0qGnWrJmx2+3m5ptvNgcPHnTr8+2335oLL7zQBAcHmzPOOMM88cQTFWp59913zVlnnWWCgoLMOeecY/7zn//U2XpbTXXb6ciRI+aKK64wUVFRpnHjxqZVq1bmtttuq7CzYjvVj8q2kyS3z6P6/Mzz9/2dzRhj6vsoEAAAQG3gHBkAAGBZBBkAAGBZBBkAAGBZBBkAAGBZBBkAAGBZBBkAAGBZBBkAAGBZBBkA8ILNZtOiRYt8XQaA/x9BBoBGjBghm81WYTj+g4GnKjMzU2FhYbUyr5oaMWKEBg4c6NMaANS+QF8XAMA/XHnllZo9e7ZbW1RUlI+qqVppaakaN27s6zIA+AmOyACQJAUHBysmJsZtaNSokSTp/fffV7du3RQSEqI2bdpoypQpOnbsmGvaadOm6dxzz1XTpk0VHx+v0aNH69ChQ5KklStX6uabb1ZRUZHrSM/kyZMlVf41TVhYmDIzMyVJu3btks1m0zvvvKOLL75YISEheuuttyRJr776qjp06KCQkBAlJSVpxowZXq3vX/7yF9199926//77FR4erpiYGFddx23fvl0XXXSRQkJC1LFjRy1fvrzCfPLy8nTdddcpLCxM4eHhGjBggHbt2iVJ+v7779WkSRPNnTvX1f/dd99VaGiotmzZ4lW9ACpHkAFQrc8++0z/+Mc/dM8992jLli166aWXlJmZqccee8zVJyAgQNOnT9fmzZs1Z84crVixQvfff78kqU+fPnr22Wdlt9u1d+9e7d27V/fdd59XNTzwwAO65557tHXrVqWmpuqtt97SxIkT9dhjj2nr1q16/PHH9fDDD2vOnDlezXfOnDlq2rSp1q5dq6lTp+qRRx5xhZXy8nINGjRIQUFBWrt2rWbOnKl//vOfbtOXlpYqNTVVzZs312effabPP/9czZo105VXXqmjR48qKSlJ//73vzV69Gjl5ubq559/1qhRo/Tkk0+qY8eOXtUKoAq+/tVKAL43fPhw06hRI9O0aVPXMGTIEGOMMZdddpl5/PHH3fq/8cYbJjY2tsr5zZ8/30RERLgez5492zgcjgr9JJmFCxe6tTkcDtcv8Obk5BhJ5tlnn3Xr07ZtWzN37ly3tkcffdQkJydXu44DBgxwPb744ovNhRde6Nbn/PPPN//85z+NMcYsW7bMBAYGmt27d7vGL1myxK3mN954w5x99tmmvLzc1aekpMSEhoaaZcuWudr69+9v+vbtay677DJzxRVXuPUHcGo4RwaAJOmSSy7Riy++6HrctGlTSdK3336rzz//3O0ITFlZmYqLi3XkyBE1adJEH3/8sTIyMvT999/L6XTq2LFjbuNPVY8ePVx/Hz58WDt27NDIkSN12223udqPHTsmh8Ph1Xw7d+7s9jg2Nlb79u2TJG3dulXx8fGKi4tzjU9OTnbr/+233+rHH39U8+bN3dqLi4u1Y8cO1+PXXntNZ511lgICArR582bZbDav6gRQNYIMAEl/BJd27dpVaD906JCmTJmiQYMGVRgXEhKiXbt26aqrrtKdd96pxx57TOHh4Vq9erVGjhypo0ePVhtkbDabjDFubaWlpZXWdmI9kvTKK6+oV69ebv2On9PjqT+fNGyz2VReXu7x9IcOHVL37t1d5+2c6MQTpb/99lsdPnxYAQEB2rt3r2JjY72qE0DVCDIAqtWtWzdt27at0pAjSRs2bFB5ebmefvppBQT8cdrdu+++69YnKChIZWVlFaaNiorS3r17XY+3b9+uI0eOVFtPdHS04uLitHPnTg0bNszb1fFYhw4dlJeX5xY81qxZ49anW7dueuedd9SyZUvZ7fZK53PgwAGNGDFCDz74oPbu3athw4bpq6++UmhoaJ3VDpxOONkXQLUmTpyo119/XVOmTNHmzZu1detWzZs3Tw899JAkqV27diotLdVzzz2nnTt36o033tDMmTPd5tG6dWsdOnRIWVlZ+vXXX11h5dJLL9Xzzz+vr7/+WuvXr9eoUaM8urR6ypQpysjI0PTp0/XDDz/ou+++0+zZszVt2rRaW++UlBSdddZZGj58uL799lt99tlnevDBB936DBs2TJGRkRowYIA+++wz5eTkaOXKlbr77rv1888/S5JGjRql+Ph4PfTQQ5o2bZrKysq8PtkZQNUIMgCqlZqaqo8++kj//e9/df7556t379565pln1KpVK0lSly5dNG3aND355JPq1KmT3nrrLWVkZLjNo0+fPho1apSuv/56RUVFaerUqZKkp59+WvHx8erbt69uvPFG3XfffR6dU3Prrbfq1Vdf1ezZs3Xuuefq4osvVmZmphITE2ttvQMCArRw4UL9/vvv6tmzp2699Va384QkqUmTJvr000+VkJCgQYMGqUOHDho5cqSKi4tlt9v1+uuva/HixXrjjTcUGBiopk2b6s0339Qrr7yiJUuW1FqtwOnMZv78BTUAAIBFcEQGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABYFkEGAABY1v8HHuKlrE9SGGMAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "\n",
    "odds_ratios = np.exp(coefficients)\n",
    "plt.bar(range(len(odds_ratios)), odds_ratios)\n",
    "plt.xlabel('Feature Index')\n",
    "plt.ylabel('Odds Ratio')\n",
    "plt.title('Odds Ratios')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 81,
   "metadata": {
    "execution": {
     "iopub.execute_input": "2024-09-25T10:28:39.140788Z",
     "iopub.status.busy": "2024-09-25T10:28:39.139934Z",
     "iopub.status.idle": "2024-09-25T10:28:55.662036Z",
     "shell.execute_reply": "2024-09-25T10:28:55.661095Z",
     "shell.execute_reply.started": "2024-09-25T10:28:39.140733Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting streamlit\n",
      "  Downloading streamlit-1.38.0-py2.py3-none-any.whl.metadata (8.5 kB)\n",
      "Requirement already satisfied: altair<6,>=4.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (5.4.1)\n",
      "Requirement already satisfied: blinker<2,>=1.0.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (1.8.2)\n",
      "Requirement already satisfied: cachetools<6,>=4.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (4.2.4)\n",
      "Requirement already satisfied: click<9,>=7.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (8.1.7)\n",
      "Requirement already satisfied: numpy<3,>=1.20 in /opt/conda/lib/python3.10/site-packages (from streamlit) (1.26.4)\n",
      "Requirement already satisfied: packaging<25,>=20 in /opt/conda/lib/python3.10/site-packages (from streamlit) (21.3)\n",
      "Requirement already satisfied: pandas<3,>=1.3.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (2.2.2)\n",
      "Requirement already satisfied: pillow<11,>=7.1.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (10.3.0)\n",
      "Requirement already satisfied: protobuf<6,>=3.20 in /opt/conda/lib/python3.10/site-packages (from streamlit) (3.20.3)\n",
      "Requirement already satisfied: pyarrow>=7.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (16.1.0)\n",
      "Requirement already satisfied: requests<3,>=2.27 in /opt/conda/lib/python3.10/site-packages (from streamlit) (2.32.3)\n",
      "Requirement already satisfied: rich<14,>=10.14.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (13.7.1)\n",
      "Requirement already satisfied: tenacity<9,>=8.1.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (8.3.0)\n",
      "Requirement already satisfied: toml<2,>=0.10.1 in /opt/conda/lib/python3.10/site-packages (from streamlit) (0.10.2)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.3.0 in /opt/conda/lib/python3.10/site-packages (from streamlit) (4.12.2)\n",
      "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/conda/lib/python3.10/site-packages (from streamlit) (3.1.43)\n",
      "Collecting pydeck<1,>=0.8.0b4 (from streamlit)\n",
      "  Downloading pydeck-0.9.1-py2.py3-none-any.whl.metadata (4.1 kB)\n",
      "Requirement already satisfied: tornado<7,>=6.0.3 in /opt/conda/lib/python3.10/site-packages (from streamlit) (6.4.1)\n",
      "Collecting watchdog<5,>=2.1.5 (from streamlit)\n",
      "  Downloading watchdog-4.0.2-py3-none-manylinux2014_x86_64.whl.metadata (38 kB)\n",
      "Requirement already satisfied: jinja2 in /opt/conda/lib/python3.10/site-packages (from altair<6,>=4.0->streamlit) (3.1.4)\n",
      "Requirement already satisfied: jsonschema>=3.0 in /opt/conda/lib/python3.10/site-packages (from altair<6,>=4.0->streamlit) (4.22.0)\n",
      "Requirement already satisfied: narwhals>=1.5.2 in /opt/conda/lib/python3.10/site-packages (from altair<6,>=4.0->streamlit) (1.8.1)\n",
      "Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/conda/lib/python3.10/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.11)\n",
      "Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in /opt/conda/lib/python3.10/site-packages (from packaging<25,>=20->streamlit) (3.1.2)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /opt/conda/lib/python3.10/site-packages (from pandas<3,>=1.3.0->streamlit) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in /opt/conda/lib/python3.10/site-packages (from pandas<3,>=1.3.0->streamlit) (2024.1)\n",
      "Requirement already satisfied: tzdata>=2022.7 in /opt/conda/lib/python3.10/site-packages (from pandas<3,>=1.3.0->streamlit) (2024.1)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in /opt/conda/lib/python3.10/site-packages (from requests<3,>=2.27->streamlit) (3.3.2)\n",
      "Requirement already satisfied: idna<4,>=2.5 in /opt/conda/lib/python3.10/site-packages (from requests<3,>=2.27->streamlit) (3.7)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/conda/lib/python3.10/site-packages (from requests<3,>=2.27->streamlit) (1.26.18)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /opt/conda/lib/python3.10/site-packages (from requests<3,>=2.27->streamlit) (2024.8.30)\n",
      "Requirement already satisfied: markdown-it-py>=2.2.0 in /opt/conda/lib/python3.10/site-packages (from rich<14,>=10.14.0->streamlit) (3.0.0)\n",
      "Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /opt/conda/lib/python3.10/site-packages (from rich<14,>=10.14.0->streamlit) (2.18.0)\n",
      "Requirement already satisfied: smmap<6,>=3.0.1 in /opt/conda/lib/python3.10/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.1)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in /opt/conda/lib/python3.10/site-packages (from jinja2->altair<6,>=4.0->streamlit) (2.1.5)\n",
      "Requirement already satisfied: attrs>=22.2.0 in /opt/conda/lib/python3.10/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (23.2.0)\n",
      "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/conda/lib/python3.10/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2023.12.1)\n",
      "Requirement already satisfied: referencing>=0.28.4 in /opt/conda/lib/python3.10/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.35.1)\n",
      "Requirement already satisfied: rpds-py>=0.7.1 in /opt/conda/lib/python3.10/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.18.1)\n",
      "Requirement already satisfied: mdurl~=0.1 in /opt/conda/lib/python3.10/site-packages (from markdown-it-py>=2.2.0->rich<14,>=10.14.0->streamlit) (0.1.2)\n",
      "Requirement already satisfied: six>=1.5 in /opt/conda/lib/python3.10/site-packages (from python-dateutil>=2.8.2->pandas<3,>=1.3.0->streamlit) (1.16.0)\n",
      "Downloading streamlit-1.38.0-py2.py3-none-any.whl (8.7 MB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m8.7/8.7 MB\u001b[0m \u001b[31m31.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m00:01\u001b[0m00:01\u001b[0m\n",
      "\u001b[?25hDownloading pydeck-0.9.1-py2.py3-none-any.whl (6.9 MB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m6.9/6.9 MB\u001b[0m \u001b[31m68.2 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m:00:01\u001b[0m00:01\u001b[0m\n",
      "\u001b[?25hDownloading watchdog-4.0.2-py3-none-manylinux2014_x86_64.whl (82 kB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m82.9/82.9 kB\u001b[0m \u001b[31m3.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
      "\u001b[?25hInstalling collected packages: watchdog, pydeck, streamlit\n",
      "Successfully installed pydeck-0.9.1 streamlit-1.38.0 watchdog-4.0.2\n"
     ]
    }
   ],
   "source": [
    "!pip install streamlit\n",
    "import streamlit as st"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kaggle": {
   "accelerator": "nvidiaTeslaT4",
   "dataSources": [
    {
     "datasetId": 153420,
     "sourceId": 352891,
     "sourceType": "datasetVersion"
    }
   ],
   "dockerImageVersionId": 30775,
   "isGpuEnabled": true,
   "isInternetEnabled": true,
   "language": "python",
   "sourceType": "notebook"
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
