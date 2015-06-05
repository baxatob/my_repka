#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json


class Track(object):
    
    def __init__(self, property_, usage):
        
        self.tabula = {
                        "User_Data": {
                            "Account": {
                                "account_number": property_["user_account_number"],
                                "account_type": property_["account_type"],
                                "Property": {
                                    "service_account": property_["service_account_number"],
                                    "address": property_["address"],
                                    "footage": property_["footage"],
                                    "enrolled_program": property_["enrolled_program"],
                                    "Usage": {
                                              usage                             
                                        }
                                    }
                                }
                            }
                        }
                    
        with open("%s.json" % property_["user_account_number"], 'w') as file_:
            file_.write(json.dumps(self.tabula))
        
        
        
        
property_ = {
                'user_account_number':"1010",
                'address':"Komsomolskaya 5a 12",
                'service_account_number':"1-987-9654",
                'footage':'3000 sqf',
                'account_type':'DOMESTIC',
                'enrolled_program':"Program # 12"
                } 

usage = [{"billing_period": "Apr 13, 2015 - May 12, 2015", "billing_usage": "596 kWh", "billing_cost": "$121.59"}, {"billing_period": "Mar 12, 2015 - Apr 13, 2015", "billing_usage": "data is unavailable", "billing_cost": "data is unavailable"}, {"billing_period": "Feb 10, 2015 - Mar 12, 2015", "billing_usage": "770 kWh", "billing_cost": "$175.36"}, {"billing_period": "Jan 12, 2015 - Feb 10, 2015", "billing_usage": "705 kWh", "billing_cost": "$156.77"}, {"billing_period": "Dec 11, 2014 - Jan 12, 2015", "billing_usage": "1,141 kWh", "billing_cost": "$300.23"}, {"billing_period": "Nov 08, 2014 - Dec 11, 2014", "billing_usage": "862 kWh", "billing_cost": "$205.78"}, {"billing_period": "Oct 09, 2014 - Nov 08, 2014", "billing_usage": "652 kWh", "billing_cost": "$141.97"}, {"billing_period": "Sep 10, 2014 - Oct 09, 2014", "billing_usage": "904 kWh", "billing_cost": "$168.07"}, {"billing_period": "Aug 11, 2014 - Sep 10, 2014", "billing_usage": "1,005 kWh", "billing_cost": "$233.00"}, {"billing_period": "Jul 11, 2014 - Aug 11, 2014", "billing_usage": "818 kWh", "billing_cost": "$171.76"}, {"billing_period": "Jun 11, 2014 - Jul 11, 2014", "billing_usage": "534 kWh", "billing_cost": "$85.75"}, {"billing_period": "May 12, 2014 - Jun 11, 2014", "billing_usage": "423 kWh", "billing_cost": "$63.57"}, {"billing_period": "Apr 11, 2014 - May 12, 2014", "billing_usage": "523 kWh", "billing_cost": "$91.87"}]

tr = Track(property_, usage)


