from lxml import html
import requests
import csv

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

page = requests.get('http://www.baressp.com.br/bares/pesquisa/?PALAVRA=show&imageField.x=0&imageField.y=0')
tree_text = page.text
elements_array = tree_text.split('<div class="GuiaEvBxCont">')

links_list = []
for element in elements_array:
	link = find_between( element, '<a href="', '">' )
	link = "http://www.baressp.com.br" + link 
	links_list.append(link)

del links_list[0]

# print links_list[2]
# page = requests.get('http://www.baressp.com.br/baladas/memphis-rock-bar')

counter = 0
total = 0
with open('email.csv', 'wb') as csvfile:
	for link in links_list:
		try:			
			page = requests.get(link)
			html_text = page.text
			html_text.lower()
			counter = counter + 1
			print counter

			if '<span class="titulo" style="font-size:12px;">E-mail: </span>' in html_text:
				total = total + 1
				print "Yup! Email disponivel!"
				print "Total de emails encontrados - " + str(total)
				post_string = html_text.split('<span class="titulo" style="font-size:12px;">E-mail: </span>',1)[1]
				email = find_between(post_string, "<a href='mailto:", '?Subject=Contato' )
				print email

				spamwriter = csv.writer(csvfile, delimiter=';')
				data = []
				data.append(email)
				spamwriter.writerows([data])

			# if total > 10:
			# 	break

		except:
			counter = counter + 1

print "__ FINITO __"
print "Total - " + str(total)
print "Counter - " + str(counter)

# http://www.baressp.com.br/baladas/memphis-rock-bar


# if 'email' in html_text:
# 	total = total + 1
# 	print "Yup! - " + str(total)
# 	post_string = html_text.split("email",1)[1]
# 	print post_string[:75]