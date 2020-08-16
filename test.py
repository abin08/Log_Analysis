import unittest
import pandas as pd
import analyze


TEST_LOG_FILE = 'test_logs'

class TestClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.df = analyze.read_logs(TEST_LOG_FILE)
        self.cleaned_df = analyze.clean(self.df)
        

    def test_read_logs(self):
        df = analyze.read_logs(TEST_LOG_FILE)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (20, 7))

    
    def test_parse_request(self):
        req = "GET /images/ksclogo-medium.gif HTTP/1.0"
        parsed_req = analyze.parse_request(req)
        self.assertEqual(parsed_req, "/images/ksclogo-medium.gif")
        parsed_req2 = analyze.parse_request(
            "GET/images/ksclogo-medium.gifHTTP/1.0")
        self.assertNotEqual(parsed_req2, "/images/ksclogo-medium.gif")

    
    def test_clean(self):
        df = analyze.read_logs(TEST_LOG_FILE)
        cleaned_df = analyze.clean(df)        
        self.assertEqual(cleaned_df.shape, (20, 5))
        
        cleaned_df_null_vals = dict(cleaned_df.isnull().sum())
        self.assertEqual(cleaned_df_null_vals, {'host': 0, 'time': 0,
            'request': 0, 'status': 0, 'content_size': 0})

        self.assertEqual(cleaned_df['status'].dtype, 'int64')
        self.assertNotEqual(cleaned_df['request'][0], 
            "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0")


    def test_top10_requests(self):
        top_10_reqs = analyze.top10_requests(self.cleaned_df)
        self.assertEqual(top_10_reqs.shape, (10, 2))
        
        count = top_10_reqs[top_10_reqs['request'] 
            == "/images/ksclogo-medium.gif"]['count'][1]
        self.assertEqual(count, 2)
        

    def test_success_req_percentage(self):
        percentage = analyze.success_req_percentage(self.cleaned_df)
        self.assertEqual(percentage, 90.0)


    def test_unsuccess_req_percentage(self):
        percentage = analyze.unsuccess_req_percentage(self.cleaned_df)
        self.assertEqual(percentage, 10.0)

    
    def test_top10_unsuccess_requests(self):
        top10_unsucc_req = analyze.top10_unsuccess_requests(self.cleaned_df)
        self.assertIsNotNone(top10_unsucc_req)


    def test_top10_hosts(self):
        top10_hosts = analyze.top10_hosts(self.cleaned_df)
        self.assertIsNotNone(top10_hosts)


    def test_top5_reqs_of_top_hosts(self):
        top_hosts_reqs = analyze.top5_reqs_of_top_hosts(self.cleaned_df)
        self.assertIsNotNone(top_hosts_reqs)