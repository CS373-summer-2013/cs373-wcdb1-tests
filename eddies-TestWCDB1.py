"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from minixsv import pyxsval
from genxmlif import GenXmlIfError
from models import Crisis, Person, Org, list_add, Li, Common
from loadModels import validate, populate_crisis, populate_person, populate_org, populate_models
from unloadModels import clean_xml, export_crisis, export_person, export_crisis, export_organization, receive_import
import xml.etree.ElementTree as ET
from django.test.client import Client
from views import passwordValidate


#xsd = open('wcdb/WorldCrises.xsd.xml', 'r')
#psvi = pyxsval.parseAndValidate("wcdb/temp.xml", "wcdb/WorldCrises.xsd.xml",
#	xmlIfClass=pyxsval.XMLIF_ELEMENTTREE)

class ModelsCrisisTest(TestCase):

#--------------------------------------------#
#-----Unit Tests for functions from models.py
#--------------------------------------------#



	#---------------------------------------#
	#-----test_li_populate

	def test_li_populate0(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		self.assertEqual(temp_li.href, "href_stuff")
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	def test_li_populate1(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.set("embed", "embed_stuff")
		temp.set("text", "text_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		self.assertEqual(temp_li.href, "href_stuff")
		self.assertEqual(temp_li.embed, "embed_stuff")
		self.assertEqual(temp_li.text, "text_stuff")
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	def test_li_populate2(self):
		temp      = ET.Element('li')
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	#---------------------------------------#
	#-----test_clean_li_xml
	
	def test_clean_li_xml0(self):
		dirt = "happy&go&lucky&&&go&happy"
		temp      = ET.Element('li')
		temp.set("href", dirt)
		temp.set("embed", dirt)
		temp.set("text", dirt)
		temp.text = dirt
		temp_li   = Li()
		temp_li.populate(temp)
		href_clean = temp_li.clean_li_xml(temp_li.href)
		embed_clean = temp_li.clean_li_xml(temp_li.embed)
		text_clean = temp_li.clean_li_xml(temp_li.text)
		floating_text_clean = temp_li.clean_li_xml(temp_li.floating_text)
		standard_clean = "happy&amp;go&amp;lucky&amp;&amp;&amp;go&amp;happy"

		self.assertEqual(href_clean, standard_clean)
		self.assertEqual(embed_clean, standard_clean)
		self.assertEqual(text_clean, standard_clean)
		self.assertEqual(floating_text_clean, standard_clean)

	def test_clean_li_xml1(self):
		dirt = "randomdirtwithoutescape"
		temp      = ET.Element('li')
		temp.set("href", dirt)
		temp.set("embed", dirt)
		temp.set("text", dirt)
		temp.text = dirt
		temp_li   = Li()
		temp_li.populate(temp)
		href_clean = temp_li.clean_li_xml(temp_li.href)
		embed_clean = temp_li.clean_li_xml(temp_li.embed)
		text_clean = temp_li.clean_li_xml(temp_li.text)
		floating_text_clean = temp_li.clean_li_xml(temp_li.floating_text)
		standard_clean = "randomdirtwithoutescape"

		self.assertEqual(href_clean, standard_clean)
		self.assertEqual(embed_clean, standard_clean)
		self.assertEqual(text_clean, standard_clean)
		self.assertEqual(floating_text_clean, standard_clean)

	def test_clean_li_xml2(self):
		dirt = "me&myself&i"
		temp      = ET.Element('li')
		temp.set("href", dirt)
		temp.set("embed", dirt)
		temp.set("text", dirt)
		temp.text = dirt
		temp_li   = Li()
		temp_li.populate(temp)
		href_clean = temp_li.clean_li_xml(temp_li.href)
		embed_clean = temp_li.clean_li_xml(temp_li.embed)
		text_clean = temp_li.clean_li_xml(temp_li.text)
		floating_text_clean = temp_li.clean_li_xml(temp_li.floating_text)
		standard_clean = "me&amp;myself&amp;i"

		self.assertEqual(href_clean, standard_clean)
		self.assertEqual(embed_clean, standard_clean)
		self.assertEqual(text_clean, standard_clean)
		self.assertEqual(floating_text_clean, standard_clean)

	#---------------------------------------#
	#-----test_li_print_xml
	
	def test_li_print_xml0(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.set("embed", "embed_stuff")
		temp.set("text", "text_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		temp_string = temp_li.print_xml()
		correct_string = "<li> href=\"href_stuff\"</li><li> embed=\"embed_stuff\"</li><li>text_stuff</li><li>randomfloatingtext</li>"
		self.assertEqual(temp_string, correct_string)

	def test_li_print_xml1(self):
		temp      = ET.Element('li')
		temp.set("href", "HELLO")
		temp.set("embed", "EMBED")
		temp.set("text", "TEXT")
		temp.text = "RANDOMTEXT"
		temp_li   = Li()
		temp_li.populate(temp)
		temp_string = temp_li.print_xml()
		correct_string = "<li> href=\"HELLO\"</li><li> embed=\"EMBED\"</li><li>TEXT</li><li>RANDOMTEXT</li>"
		self.assertEqual(temp_string, correct_string)

	def test_li_print_xml2(self):
		temp      = ET.Element('li')
		temp.set("href", "fee")
		temp.set("embed", "foo")
		temp.set("text", "fi")
		temp.text = "fum"
		temp_li   = Li()
		temp_li.populate(temp)
		temp_string = temp_li.print_xml()
		correct_string = "<li> href=\"fee\"</li><li> embed=\"foo\"</li><li>fi</li><li>fum</li>"
		self.assertEqual(temp_string, correct_string)

	#---------------------------------------#
	#-----test_common_populate

	def test_common_populate0(self):
		temp_com = Common()
		xml_string = '<Common><Citations><li>The Hindustan Times</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><Images><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Videos><li embed="//www.youtube.com/embed/qV3s7Sa6B6w" /></Videos><Maps><li embed="https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed" /></Maps><Feeds><li embed="[WHATEVER A FEED URL LOOKS LIKE]" /></Feeds><Summary>Lorem ipsum...</Summary></Common>'
		root = ET.fromstring(xml_string)
		temp_com.populate(root)

		self.assertEqual(temp_com.citations[0].floating_text, "The Hindustan Times")
		self.assertEqual(temp_com.external_links[0].href, "http://en.wikipedia.org/wiki/2013_North_India_floods")
		self.assertEqual(temp_com.images[0].embed, "http://timesofindia.indiatimes.com/photo/15357310.cms")
		self.assertEqual(temp_com.videos[0].embed, "//www.youtube.com/embed/qV3s7Sa6B6w")
		#self.assertEqual(temp_com.maps[0].href, "https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed")
		self.assertEqual(temp_com.feeds[0].embed, "[WHATEVER A FEED URL LOOKS LIKE]")
		self.assertEqual(temp_com.videos[0].embed, "//www.youtube.com/embed/qV3s7Sa6B6w")

	def test_common_populate1(self):
		temp_com = Common()
		xml_string = '<Common><Citations><li>Random Citation</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><Images><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Summary>Random Summary</Summary></Common>'
		root = ET.fromstring(xml_string)
		temp_com.populate(root)

		self.assertEqual(temp_com.citations[0].floating_text, "Random Citation")
		self.assertEqual(temp_com.external_links[0].href, "http://en.wikipedia.org/wiki/2013_North_India_floods")
		self.assertEqual(temp_com.images[0].embed, "http://timesofindia.indiatimes.com/photo/15357310.cms")
		#self.assertEqual(temp_com.videos[0], "Random Summary")
	
	def test_common_populate2(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>Random Citation</li></Citations><Summary>Random Summary</Summary></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)

		self.assertEqual(temp_com.citations[0].floating_text, "Random Citation")

	#---------------------------------------#
	#-----test_xml_from_li

	def test_xml_from_li0(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>RandomCitation</li></Citations><ExternalLinks><li>RandomLink</li></ExternalLinks><Images><li>RandomImage</li></Images><Videos><li>RandomVideo</li></Videos></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		li_xml = "<Common>"
		c_cites = temp_com.xml_from_li("Citations", temp_com.citations)
		li_xml += c_cites
		c_links = temp_com.xml_from_li("ExternalLinks", temp_com.external_links)
		li_xml += c_links
		c_ims = temp_com.xml_from_li("Images", temp_com.images)
		li_xml += c_ims
		c_vids = temp_com.xml_from_li("Videos", temp_com.videos)
		li_xml += c_vids
		li_xml += "</Common>"
		self.assertEqual(li_xml, xml_string )

	def test_xml_from_li1(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>Citation</li></Citations><ExternalLinks><li>Link</li></ExternalLinks><Images><li>Image</li></Images><Videos><li>Video</li></Videos></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		li_xml = "<Common>"
		c_cites = temp_com.xml_from_li("Citations", temp_com.citations)
		li_xml += c_cites
		c_links = temp_com.xml_from_li("ExternalLinks", temp_com.external_links)
		li_xml += c_links
		c_ims = temp_com.xml_from_li("Images", temp_com.images)
		li_xml += c_ims
		c_vids = temp_com.xml_from_li("Videos", temp_com.videos)
		li_xml += c_vids
		li_xml += "</Common>"
		self.assertEqual(li_xml, xml_string )

	def test_xml_from_li2(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>dvfjnkjdnv</li></Citations><ExternalLinks><li>sdcbkjsnbd</li></ExternalLinks><Images><li>efvdjkjnfv</li></Images><Videos><li>dfvnldkfjvnbo</li></Videos></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		li_xml = "<Common>"
		c_cites = temp_com.xml_from_li("Citations", temp_com.citations)
		li_xml += c_cites
		c_links = temp_com.xml_from_li("ExternalLinks", temp_com.external_links)
		li_xml += c_links
		c_ims = temp_com.xml_from_li("Images", temp_com.images)
		li_xml += c_ims
		c_vids = temp_com.xml_from_li("Videos", temp_com.videos)
		li_xml += c_vids
		li_xml += "</Common>"
		self.assertEqual(li_xml, xml_string )

	#---------------------------------------#
	#-----test_print_xml
	
	def test_print_xml0(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>RandomCitation</li></Citations><ExternalLinks><li>RandomLink</li></ExternalLinks><Images><li>RandomImage</li></Images><Videos><li>RandomVideo</li></Videos><Summary>Random Summary</Summary></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		common_xml = temp_com.print_xml()

		self.assertEqual(xml_string, common_xml)

	def test_print_xml1(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>Citation</li></Citations><ExternalLinks><li>Link</li></ExternalLinks><Images><li>Image</li></Images><Videos><li>Video</li></Videos></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		common_xml = temp_com.print_xml()

		self.assertEqual(xml_string, common_xml)

	def test_print_xml2(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>dvfjnkjdnv</li></Citations><ExternalLinks><li>sdcbkjsnbd</li></ExternalLinks><Images><li>efvdjkjnfv</li></Images><Videos><li>dfvnldkfjvnbo</li></Videos></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		common_xml = temp_com.print_xml()

		self.assertEqual(xml_string, common_xml)




class unloadModelsCrisisTest(TestCase):

#---------------------------------------------------#
#-----Unit Tests for functions from unloadModels.py
#---------------------------------------------------#

	#---------------------------------------#
	#-----test_clean_xml (paranoid clean for things that are not li objects)
	
	def test_clean_xml0(self):
		dirt = "happy&go&lucky&&&go&happy"
		dirt_to_clean = clean_xml(dirt)
		standard_clean = "happy&amp;go&amp;lucky&amp;&amp;&amp;go&amp;happy"
		self.assertEqual(dirt_to_clean, standard_clean)

	def test_clean_xml1(self):
		dirt = "randomdirtwithoutescape"
		dirt_to_clean = clean_xml(dirt)
		standard_clean = "randomdirtwithoutescape"
		self.assertEqual(dirt_to_clean, standard_clean)

	def test_clean_xml2(self):
		dirt = "me&myself&i"
		dirt_to_clean = clean_xml(dirt)
		standard_clean = "me&amp;myself&amp;i"
		self.assertEqual(dirt_to_clean, standard_clean)
	
	#---------------------------------------#
	#-----test_export_crisis

	def test_export_crisis0(self):
		xml_string = "<WC><Crisis ID=\"CRI_random\" Name=\"random\"><People><Person ID=\"PER_random\" /></People><Organizations><Org ID=\"ORG_random\" /></Organizations><Kind>random</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>random</li></Locations><HumanImpact><li>random</li></HumanImpact><EconomicImpact><li>random</li></EconomicImpact><ResourcesNeeded><li>random</li></ResourcesNeeded><WaysToHelp><li> href=\"http://random\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis></WC>"
		crisis_list1 = []
		root1 = ET.fromstring(xml_string)
		populate_crisis(root1, crisis_list1)
		
		crisis_xml = export_crisis(crisis_list1[0])
		check_string = xml_string [4:-5]
		self.assertEqual(check_string, crisis_xml)

	def test_export_crisis1(self):
		xml_string = "<WC><Crisis ID=\"CRI_CRISISCHECK\" Name=\"CRISISCHECK\"><People><Person ID=\"PER_CRISISCHECK\" /></People><Organizations><Org ID=\"ORG_CRISISCHECK\" /></Organizations><Kind>CRISISCHECK</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>CRISISCHECK</li></Locations><HumanImpact><li>CRISISCHECK</li></HumanImpact><EconomicImpact><li>CRISISCHECK</li></EconomicImpact><ResourcesNeeded><li>CRISISCHECK</li></ResourcesNeeded><WaysToHelp><li> href=\"http://CRISISCHECK\"</li><li>CRISISCHECK</li></WaysToHelp><Common><Citations><li> href= CRISISCHECK</li></Citations><ExternalLinks><li> href=\"http:CRISISCHECK.html\"</li></ExternalLinks><Images><li> embed=\"http:CRISISCHECK.jpg\"</li></Images><Summary>CRISISCHECK</Summary></Common></Crisis></WC>"
		crisis_list1 = []
		root1 = ET.fromstring(xml_string)
		populate_crisis(root1, crisis_list1)
		
		crisis_xml = export_crisis(crisis_list1[0])
		check_string = xml_string [4:-5]
		self.assertEqual(check_string, crisis_xml)

	def test_export_crisis2(self):
		xml_string = "<WC><Crisis ID=\"CRI_important\" Name=\"important\"><People><Person ID=\"PER_important\" /></People><Organizations><Org ID=\"ORG_important\" /></Organizations><Kind>important</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>important</li></Locations><HumanImpact><li>important</li></HumanImpact><EconomicImpact><li>important</li></EconomicImpact><ResourcesNeeded><li>important</li></ResourcesNeeded><WaysToHelp><li> href=\"http://important\"</li><li>important</li></WaysToHelp><Common><Citations><li> href= important</li></Citations><ExternalLinks><li> href=\"http:important.html\"</li></ExternalLinks><Images><li> embed=\"http:important.jpg\"</li></Images><Summary>important</Summary></Common></Crisis></WC>"
		crisis_list1 = []
		root1 = ET.fromstring(xml_string)
		populate_crisis(root1, crisis_list1)
		
		crisis_xml = export_crisis(crisis_list1[0])
		check_string = xml_string [4:-5]
		self.assertEqual(check_string, crisis_xml)


	#---------------------------------------#
	#-----test_export_person

	def test_export_person0(self):
		person_string = "<WC><Person ID=\"PER_HMUBAR\" Name=\"Hosni Mubarak\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		person_list = []
		root = ET.fromstring(person_string)
		populate_person(root, person_list)
		person_xml = export_person(person_list[0])
		check_string = person_string [4:-5]

		self.assertEqual(check_string, person_xml)

	def test_export_person1(self):
		person_string = "<WC><Person ID=\"PER_ELBARA\" Name=\"Mohamed ElBaradei\"><Crises><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		person_list = []
		root = ET.fromstring(person_string)
		populate_person(root, person_list)
		person_xml = export_person(person_list[0])
		check_string = person_string [4:-5]

		self.assertEqual(check_string, person_xml)

	def test_export_person2(self):
		person_string = "<WC><Person ID=\"PER_MMORSI\" Name=\"Mohammed Morsi\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_MUSBRO\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		person_list = []
		root = ET.fromstring(person_string)
		populate_person(root, person_list)
		person_xml = export_person(person_list[0])
		check_string = person_string [4:-5]

		self.assertEqual(check_string, person_xml)

	#---------------------------------------#
	#-----test_export_organization

	def test_export_org0(self):
		org_string = "<WC><Organization ID=\"ORG_MUSBRO\" Name=\"The Muslim Brotherhood\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><People><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_MMORSI\" /></People><Kind>Islamic Movement</Kind><Location>Egypt</Location><Common></Common></Organization></WC>"
		org_list = []
		root8 = ET.fromstring(org_string)
		populate_org(root8, org_list)
		org_xml = export_organization(org_list[0])
		check_string = org_string [4:-5]

		self.assertEqual(check_string, org_xml)

	def test_export_org1(self):
		org_string = "<WC><Organization ID=\"ORG_random\" Name=\"random\"><Crises><Crisis ID=\"CRI_random\" /></Crises><People><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /></People><Kind>random</Kind><Location>random</Location><Common></Common></Organization></WC>"
		check_string = org_string [4:-5]
		org_list = []
		root8 = ET.fromstring(org_string)
		populate_org(root8, org_list)
		org_xml = export_organization(org_list[0])

		self.assertEqual(check_string, org_xml)

	def test_export_org2(self):
		org_string = "<WC><Organization ID=\"ORG_ORGANIZE\" Name=\"ORGANIZE\"><Crises><Crisis ID=\"CRI_ORGANIZE\" /></Crises><People><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /></People><Kind>ORGANIZE</Kind><Location>ORGANIZE</Location><Common></Common></Organization></WC>"
		check_string = org_string [4:-5]
		org_list = []
		root8 = ET.fromstring(org_string)
		populate_org(root8, org_list)
		org_xml = export_organization(org_list[0])

		self.assertEqual(check_string, org_xml)


class loadModelsCrisisTest(TestCase):

#------------------------------------------------#
#-----Unit Tests for functions from loadModels.py
#------------------------------------------------#

	#---------------------------------------#
	#-----test_validate

	def test_validate0(self):
		f = open('wcdb/xml0.xml')
		self.assertEqual(type(f), file)
		self.assert_(validate(f) != False)

	def test_validate1(self):
		f = open('wcdb/xml1.xml')
		self.assertEqual(type(f), file)
		self.assert_(type(validate(f)) == str)

	def test_validate2(self):
		f = open('wcdb/xml2.xm')
		self.assertEqual(type(f), file)
		self.assertEqual(validate(f), False)

	#---------------------------------------#
	#-----test_populate_models

	def populate_models0(self) :
		crisis_string = "<WC><Crisis ID=\"CRI_NOTFOREXPORT\" Name=\"NOTFOREXPORT\"><People><Person ID=\"PER_NOTFOREXPORT\" /></People><Organizations><Org ID=\"ORG_NOTFOREXPORT\" /></Organizations><Kind>NOTFOREXPORT</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>random</li></Locations><HumanImpact><li>random</li></HumanImpact><EconomicImpact><li>random</li></EconomicImpact><ResourcesNeeded><li>random</li></ResourcesNeeded><WaysToHelp><li> href=\"http://random\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis>"
		person_string = "<Person ID=\"PER_HMUBAR\" Name=\"Hosni Mubarak\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person>"
		org_string = "<Organization ID=\"ORG_MUSBRO\" Name=\"The Muslim Brotherhood\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><People><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_MMORSI\" /></People><Kind>Islamic Movement</Kind><Location>Egypt</Location><Common></Common></Organization></WC>"
		xml_to_tree = crisis_string + person_string + org_string
		e_tree = ET.parse(xml_to_tree)
		cri_per_org_dict = populate_models(e_tree)
		print "TYPE DICT = ", type(cri_per_org_dict)
		#self.assertEqual(type(cri_per_org_dict), )


	def populate_models1(self) :
		crisis_string = "<WC><Crisis ID=\"CRI_kindofrandom\" Name=\"kindofrandom\"><People><Person ID=\"PER_kindofrandom\" /></People><Organizations><Org ID=\"ORG_kindofrandom\" /></Organizations><Kind>kindofrandom</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>kindofrandom</li></Locations><HumanImpact><li>kindofrandom</li></HumanImpact><EconomicImpact><li>kindofrandom</li></EconomicImpact><ResourcesNeeded><li>kindofrandom</li></ResourcesNeeded><WaysToHelp><li> href=\"http://kindofrandom\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis>"
		person_string = "<Person ID=\"PER_ELBARA\" Name=\"Mohamed ElBaradei\"><Crises><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person>"
		org_string = "<Organization ID=\"ORG_random\" Name=\"random\"><Crises><Crisis ID=\"CRI_random\" /></Crises><People><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /></People><Kind>random</Kind><Location>random</Location><Common></Common></Organization></WC>"
		xml_to_tree = crisis_string + person_string + org_string
		e_tree = ET.parse(xml_to_tree)
		populate_models(e_tree)

	def populate_models2(self) :
		crisis_string = "<WC><Crisis ID=\"CRI_last_populate_crisis_to_check\" Name=\"last_populate_crisis_to_check\"><People><Person ID=\"PER_last_populate_crisis_to_check\" /></People><Organizations><Org ID=\"ORG_last_populate_crisis_to_check\" /></Organizations><Kind>last_populate_crisis_to_check</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>last_populate_crisis_to_check</li></Locations><HumanImpact><li>last_populate_crisis_to_check</li></HumanImpact><EconomicImpact><li>last_populate_crisis_to_check</li></EconomicImpact><ResourcesNeeded><li>last_populate_crisis_to_check</li></ResourcesNeeded><WaysToHelp><li> href=\"http://last_populate_crisis_to_check\"</li><li>last_populate_crisis_to_check</li></WaysToHelp><Common><Citations><li> href= last_populate_crisis_to_check</li></Citations><ExternalLinks><li> href=\"http:last_populate_crisis_to_check.html\"</li></ExternalLinks><Images><li> embed=\"http:last_populate_crisis_to_check.jpg\"</li></Images><Summary>last_populate_crisis_to_check</Summary></Common></Crisis>"
		person_string = "<Person ID=\"PER_MMORSI\" Name=\"Mohammed Morsi\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_MUSBRO\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person>"
		org_string = "<Organization ID=\"ORG_ORGANIZE\" Name=\"ORGANIZE\"><Crises><Crisis ID=\"CRI_ORGANIZE\" /></Crises><People><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /></People><Kind>ORGANIZE</Kind><Location>ORGANIZE</Location><Common></Common></Organization></WC>"
		xml_to_tree = crisis_string + person_string + org_string
		e_tree = ET.parse(xml_to_tree)
		populate_models(e_tree)


	#---------------------------------------#
	#-----test_populate_crisis

	def test_populate_crisis0(self):
		xml_string = "<WC><Crisis ID=\"CRI_NOTFOREXPORT\" Name=\"NOTFOREXPORT\"><People><Person ID=\"PER_NOTFOREXPORT\" /></People><Organizations><Org ID=\"ORG_NOTFOREXPORT\" /></Organizations><Kind>NOTFOREXPORT</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>random</li></Locations><HumanImpact><li>random</li></HumanImpact><EconomicImpact><li>random</li></EconomicImpact><ResourcesNeeded><li>random</li></ResourcesNeeded><WaysToHelp><li> href=\"http://random\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis></WC>"
		crisis_list = []
		root = ET.fromstring(xml_string)
		populate_crisis(root, crisis_list)

		self.assert_(len(crisis_list) >= 1)

	def test_populate_crisis1(self):
		xml_string1 = "<WC><Crisis ID=\"CRI_kindofrandom\" Name=\"kindofrandom\"><People><Person ID=\"PER_kindofrandom\" /></People><Organizations><Org ID=\"ORG_kindofrandom\" /></Organizations><Kind>kindofrandom</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>kindofrandom</li></Locations><HumanImpact><li>kindofrandom</li></HumanImpact><EconomicImpact><li>kindofrandom</li></EconomicImpact><ResourcesNeeded><li>kindofrandom</li></ResourcesNeeded><WaysToHelp><li> href=\"http://kindofrandom\"</li><li>random</li></WaysToHelp><Common><Citations><li> href= random</li></Citations><ExternalLinks><li> href=\"http:random.html\"</li></ExternalLinks><Images><li> embed=\"http:random.jpg\"</li></Images><Summary>random</Summary></Common></Crisis></WC>"
		crisis_list1 = []
		root1 = ET.fromstring(xml_string1)
		populate_crisis(root1, crisis_list1)

		self.assert_(len(crisis_list1) >= 1)

	def test_populate_crisis2(self):
		xml_string1 = "<WC><Crisis ID=\"CRI_last_populate_crisis_to_check\" Name=\"last_populate_crisis_to_check\"><People><Person ID=\"PER_last_populate_crisis_to_check\" /></People><Organizations><Org ID=\"ORG_last_populate_crisis_to_check\" /></Organizations><Kind>last_populate_crisis_to_check</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>last_populate_crisis_to_check</li></Locations><HumanImpact><li>last_populate_crisis_to_check</li></HumanImpact><EconomicImpact><li>last_populate_crisis_to_check</li></EconomicImpact><ResourcesNeeded><li>last_populate_crisis_to_check</li></ResourcesNeeded><WaysToHelp><li> href=\"http://last_populate_crisis_to_check\"</li><li>last_populate_crisis_to_check</li></WaysToHelp><Common><Citations><li> href= last_populate_crisis_to_check</li></Citations><ExternalLinks><li> href=\"http:last_populate_crisis_to_check.html\"</li></ExternalLinks><Images><li> embed=\"http:last_populate_crisis_to_check.jpg\"</li></Images><Summary>last_populate_crisis_to_check</Summary></Common></Crisis></WC>"
		crisis_list1 = []
		root1 = ET.fromstring(xml_string1)
		populate_crisis(root1, crisis_list1)

		self.assert_(len(crisis_list1) >= 1)


	#---------------------------------------#
	#-----test_populate_person

	def test_populate_person0(self):
		xml_string = "<WC><Person ID=\"PER_HMUBAR\" Name=\"Hosni Mubarak\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		person_list = []
		root = ET.fromstring(xml_string)
		populate_person(root, person_list)

	 	self.assert_(len(person_list) >= 1)

	def test_populate_person1(self):
		xml_string1 = "<WC><Person ID=\"PER_ELBARA\" Name=\"Mohamed ElBaradei\"><Crises><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		person_list1 = []
		root1 = ET.fromstring(xml_string1)
		populate_person(root1, person_list1)

		self.assert_(len(person_list1) >= 1)

	def test_populate_person2(self):
		xml_string = "<WC><Person ID=\"PER_MMORSI\" Name=\"Mohammed Morsi\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_EGYGOV\" /><Org ID=\"ORG_MUSBRO\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		person_list = []
		root = ET.fromstring(xml_string)
		populate_person(root, person_list)

	 	self.assert_(len(person_list) >= 1)

	#---------------------------------------#
	#-----test_populate_org

	def test_populate_org0(self):
		xml_string = "<WC><Organization ID=\"ORG_MUSBRO\" Name=\"The Muslim Brotherhood\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><People><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_MMORSI\" /></People><Kind>Islamic Movement</Kind><Location>Egypt</Location><Common></Common></Organization></WC>"
		org_list = []
		root = ET.fromstring(xml_string)
		populate_org(root, org_list)

	 	self.assert_(len(org_list) >= 1)

	def test_populate_org1(self):
		xml_string1 = "<WC><Organization ID=\"ORG_random\" Name=\"random\"><Crises><Crisis ID=\"CRI_random\" /></Crises><People><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /><Person ID=\"PER_random\" /></People><Kind>random</Kind><Location>random</Location><Common></Common></Organization></WC>"
		org_list1 = []
		root1 = ET.fromstring(xml_string1)
		populate_org(root1, org_list1)

		self.assert_(len(org_list1) >= 1)

	def test_populate_org2(self):
		xml_string = "<WC><Organization ID=\"ORG_ORGANIZE\" Name=\"ORGANIZE\"><Crises><Crisis ID=\"CRI_ORGANIZE\" /></Crises><People><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /><Person ID=\"PER_ORGANIZE\" /></People><Kind>ORGANIZE</Kind><Location>ORGANIZE</Location><Common></Common></Organization></WC>"
		org_list = []
		root = ET.fromstring(xml_string)
		populate_org(root, org_list)

	 	self.assert_(len(org_list) >= 1)


class viewsTest(TestCase):

#--------------------------------------------#
#-----Unit Tests for functions from views.py
#--------------------------------------------#

	#---------------------------------------#
	#-----test_crisisView
	#---------------------------------------#

	# tests that user can see our pages 
	def test_indexView(self):
		response = self.client.get("http://localhost:8000/")
		self.assertEqual(response.status_code, 200)

	def test_crisisView0(self):
		response = self.client.get("http://localhost:8000/crisis/1")
		self.assertEqual(response.status_code, 200)

	def test_crisisView1(self):
		response = self.client.get("http://localhost:8000/crisis/2")
		self.assertEqual(response.status_code, 200)

	def test_crisisView2(self):
		response = self.client.get("http://localhost:8000/crisis/3")
		self.assertEqual(response.status_code, 200)

	def test_orgsView0(self):
		response = self.client.get("http://localhost:8000/orgs/1")
		self.assertEqual(response.status_code, 200)

	def test_orgsView1(self):
		response = self.client.get("http://localhost:8000/orgs/2")
		self.assertEqual(response.status_code, 200)

	def test_orgsView2(self):
		response = self.client.get("http://localhost:8000/orgs/3")
		self.assertEqual(response.status_code, 200)

	def test_peopleView0(self):
		response = self.client.get("http://localhost:8000/people/1")
		self.assertEqual(response.status_code, 200)

	def test_peopleView1(self):
		response = self.client.get("http://localhost:8000/people/2")
		self.assertEqual(response.status_code, 200)

	def test_peopleView2(self):
		response = self.client.get("http://localhost:8000/people/3")
		self.assertEqual(response.status_code, 200)

	"""
	Creates an infinite loop!
	def test_unittestView(self):
		response = self.client.get("http://localhost:8000/unittests/")
		self.assertEqual(response.status_code, 200)
	"""

	def test_importView1(self):
		response = self.client.get("http://localhost:8000/import/")
		self.assertEqual(response.status_code, 200)

	def test_importView2(self):
		c = Client()
		with open('wcdb/xml0.xml') as upload:
			response = self.client.post("http://localhost:8000/import/", {'password': "ateam", 'xmlvalue': upload}, follow = True)
        	self.assertEqual(response.status_code, 200) # Redirect on form success

	def test_passwordValidate0(self):
		pw = "ateam"
		result = passwordValidate(pw)
		self.assert_(result)

	def test_passwordValidate1(self):
		pw = "someotherteam"
		result = passwordValidate(pw)
		self.assert_(not (result))

	def test_exportView(self):
		response = self.client.get("http://127.0.0.1:8000/export/")
		self.assertEqual(response.status_code, 200)
