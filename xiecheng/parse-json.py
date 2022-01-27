import json

if __name__ == '__main__':
    with open("xiecheng.json", 'r') as load_f:
        plan_json = json.load(load_f)
    if plan_json:
        flightItineraryList = plan_json['data']['flightItineraryList']
        for fi in flightItineraryList:
            flightList = fi['flightSegments'][0]['flightList'][0]
            priceList = fi['priceList']
            if flightList['marketAirlineName'] != '中国国航':
                continue

            msg = flightList['marketAirlineName'] + " " + flightList['flightNo'] + flightList['aircraftName'] + "\n" + \
                  flightList['departureDateTime'] + " = " + flightList['arrivalDateTime'] + "\t\t\t" \
                  + "¥" + str(priceList[0]['adultPrice']) + "\n" + \
                  flightList['departureAirportName'] + "\t\t\t" + flightList['arrivalAirportName'] + "\n"
            print(msg)
    print()
