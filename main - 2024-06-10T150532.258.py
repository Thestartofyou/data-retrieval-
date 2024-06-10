import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Google Analytics setup
def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'path_to_credentials.json', ['https://www.googleapis.com/auth/analytics.readonly']
    )
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics

def get_analytics_data(analytics):
    response = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': 'YOUR_VIEW_ID',
                    'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'}, {'expression': 'ga:bounceRate'}, {'expression': 'ga:pageviews'}]
                }
            ]
        }
    ).execute()
    return response

# Twitter setup
def get_twitter_data(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = "https://api.twitter.com/2/users/by/username/YOUR_USERNAME?user.fields=public_metrics"
    response = requests.get(url, headers=headers)
    return response.json()

# Facebook setup
def get_facebook_data(access_token, page_id):
    url = f"https://graph.facebook.com/v11.0/{page_id}/insights?metric=page_impressions,page_engaged_users&access_token={access_token}"
    response = requests.get(url)
    return response.json()

# Stripe setup
def get_stripe_data(api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.stripe.com/v1/charges"
    response = requests.get(url, headers=headers)
    return response.json()

# Fetch data
analytics = initialize_analyticsreporting()
ga_data = get_analytics_data(analytics)
twitter_data = get_twitter_data('YOUR_TWITTER_BEARER_TOKEN')
facebook_data = get_facebook_data('YOUR_FACEBOOK_ACCESS_TOKEN', 'YOUR_PAGE_ID')
stripe_data = get_stripe_data('YOUR_STRIPE_API_KEY')

# Process Google Analytics data
ga_sessions = ga_data['reports'][0]['data']['totals'][0]['values'][0]
ga_bounce_rate = ga_data['reports'][0]['data']['totals'][0]['values'][1]
ga_pageviews = ga_data['reports'][0]['data']['totals'][0]['values'][2]

# Process Twitter data
twitter_followers = twitter_data['data']['public_metrics']['followers_count']
twitter_tweets = twitter_data['data']['public_metrics']['tweet_count']

# Process Facebook data
fb_impressions = facebook_data['data'][0]['values'][0]['value']
fb_engagement = facebook_data['data'][1]['values'][0]['value']

# Process Stripe data
total_sales = sum([charge['amount'] for charge in stripe_data['data']]) / 100  # Assuming amount is in cents
num_sales = len(stripe_data['data'])

# Create a consolidated DataFrame
data = {
    'Metric': ['GA Sessions', 'GA Bounce Rate', 'GA Pageviews', 'Twitter Followers', 'Twitter Tweets', 'FB Impressions', 'FB Engagement', 'Total Sales', 'Number of Sales'],
    'Value': [ga_sessions, ga_bounce_rate, ga_pageviews, twitter_followers, twitter_tweets, fb_impressions, fb_engagement, total_sales, num_sales]
}
df = pd.DataFrame(data)

# Visualization
plt.figure(figsize=(14, 8))
sns.barplot(x='Metric', y='Value', data=df)
plt.title('Startup Performance Metrics')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

