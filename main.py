from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db


class ParkingSpot(db.Model):	
	company_name =  db.StringProperty(required=True)
	spot_id =  db.StringProperty(required=False)


class Reservation(db.Model):	
	company_name =  db.StringProperty(required=True)
	spot_id =  db.StringProperty(required=False)
	emp_name = db.StringProperty(required=False)
	day = db.StringProperty(required=False)


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<h2>Parkimatic</h2>Welcome to Parkimatic, we make parking easy!<br>Go to your comapny\'s name via the url like: http://parkimatic.appspot.com/Matomy<br>Or go to your own reservations via the url like: http://parkimatic.appspot.com/my/Gal')

		

class FetchSpotsPerCompany(webapp.RequestHandler):
    def get(self, company):

	all_spots = "<h1 ><a href='/'>Parkimatic</a></h1><h2>" + company + "</h2><u>Reserve a parking spot</u><br><br>"
	
	all_spots += '<form action="/reserve">'
	all_spots += 'Employee Name:<br><input name="emp_name" maxlength="80" size="80"/><br><br>'
	all_spots += 'day to reserve:<br><input name="day" maxlength="8" size="8"/>(dd.mm.yy)<br><br>'
	all_spots += '<input type="hidden" name="company_name" value="'+company+'"/>'
	all_spots += '<br><input type="submit" value="Reserve"/>'
	all_spots += '</form>'
	
	all_spots += "<hr><h2>" + company + "'s spots</h2>"
	
	query_results = ParkingSpot.gql("WHERE company_name = :company_name order by spot_id", company_name=company)
	
	for result in query_results:
		all_spots += "-"+result.spot_id + "<br>"
	

	
	#print all_spots
	
        template_values = {
            'all_spots': all_spots,
        }

	self.response.out.write(all_spots)

			

class FetchReservationsPerEmployee(webapp.RequestHandler):
    def get(self, emp_name):

	all_spots = "<h1><a href='/'>Parkimatic</a></h1>"
	
	all_spots += "<h2>" + emp_name + "'s spots</h2>"
	
	query_results = Reservation.gql("WHERE emp_name = :emp_name", emp_name=emp_name)
	
	for result in query_results:
		all_spots += result.day +"  -  "+result.spot_id + " at " + result.company_name +"<br>"
	

	
	#print all_spots
	
        template_values = {
            'all_spots': all_spots,
        }

	self.response.out.write(all_spots)

			
		
class AddInitialData(webapp.RequestHandler):
    def get(self):
	#this class adds demo parking_spots

	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p1") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p2") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p3") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p4") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p5") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p6") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p7") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p8") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p9") 
	parking_spot.put()
	parking_spot = ParkingSpot(company_name = "Matomy",spot_id = "p10") 
	parking_spot.put()

		
	template_values = {
            'parking_spot': parking_spot,
        }
		
	self.response.out.write(parking_spot)




class Reserve(webapp.RequestHandler):
    def get(self):
	#this class reserves
	#reservations_query_results = Reservation.gql("WHERE company_name = :company_name and day= :day", company_name = self.request.get('company_name'),day = self.request.get('day'))
	spots_query_results = ParkingSpot.gql("WHERE company_name = :company_name", company_name = self.request.get('company_name'))
	
	for result in spots_query_results:
		found_taken_spot = Reservation.gql("WHERE company_name = :company_name and day = :day and spot_id = :spot_id", company_name = self.request.get('company_name'),day = self.request.get('day'),spot_id=result.spot_id).get()
		if found_taken_spot == None:
			empty_spot = result.spot_id
			break
				
	
	#empty_spot = "p3"
	reservation = Reservation(company_name = self.request.get('company_name'),emp_name = self.request.get('emp_name'),day = self.request.get('day'),spot_id = empty_spot)
	reservation.put()
	response = "/my/"+self.request.get('emp_name')
	
		
	template_values = {
            'response': response,
        }
		
	self.redirect(response)		



def main():
    application = webapp.WSGIApplication([('/', MainHandler),
											('/addinitialdata1987', AddInitialData),
											('/reserve', Reserve),
											('/my/(.+)', FetchReservationsPerEmployee),
											('/(.+)', FetchSpotsPerCompany),
										 ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
