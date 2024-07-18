from bs4 import BeautifulSoup
# from llamaindex import SimpleIndexer
import numpy as np

# Function to parse HTML and split into chunks
def parse_and_split_html(html_content, chunk_size=100):
    soup = BeautifulSoup(html_content.replace('<\/','</'), 'html.parser')
    texts = soup.get_text(separator='\n######\n')
    
    print(len(texts.split('\n######\n')))
    # Split text into chunks
    words = texts.split('\n######\n')
    # chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    chunks = [word.strip() for word in words if (word != ' ')]
    # previous_word_append_flag = False
    # for i,word in enumerate(words): 
    #     if (word != ' '):
    #         if len(word.split(' '))<5:
    #             chunk += word
    #             previous_word_append_flag = True
    #         else:
    #             chunk = word  
    #             previous_word_append_flag = False
    #         if previous_word_append_flag != True:
    #             chunks.append(chunk)

    return chunks

def html_split_knowledge_graph(html_content, chunk_size=100):
    soup = BeautifulSoup(html_content.replace('<\/','</'), 'html.parser')
    chunks = parse_and_split_html(html_content)
    headers = {}
    headers_arr = []
    
    for level in range(1,7):
        header_tag = f'h{level}'
        headers[header_tag] = [header.get_text(strip=True) for header in soup.find_all(header_tag) if header.get_text(strip=True)]
        if headers[header_tag]:
            headers_arr.extend(headers[header_tag])
    
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]

    # Print the headers
    # for level, texts in headers.items():
    #     print(f"{level.upper()}:")
    #     for text in texts:
    #         print(f"  {text}")

    level = 0
    j=0
    h=0
    kg_chunks = {}
    para_chunks = []
    header_name = ""
    # print(chunks[:50])
    print(headers)
    for chunk in chunks:
        # print(headers_arr[h])
        if chunk ==  headers_arr[h]:
            if len(para_chunks) != 0:
                kg_chunks[header_name] = para_chunks
                para_chunks = []
            elif header_name:
                kg_chunks[header_name] = chunk
            header_name = chunk
            # print(header_name)
            h += 1  
        if chunk == paragraphs[j]:
            # print(chunk)
            para_chunks.append(chunk)
            j += 1 
            if j == len(paragraphs):
                if len(para_chunks) != 0:
                    kg_chunks[header_name] = para_chunks
                break
    print(kg_chunks)
    print(paragraphs[-1])
    # print(headers_arr)
     
# Example HTML content
html_content = """
Email marketing - Wikipedia <H1> Email marketing <\/H1> Jump to : navigation , search <Table> <Tr> <Td> <\/Td> <Td> ( hide ) This article has multiple issues . Please help improve it or discuss these issues on the talk page . ( Learn how and when to remove these template messages ) <Table> <Tr> <Td> <\/Td> <Td> This article needs additional citations for verification . Please help improve this article by adding citations to reliable sources . Unsourced material may be challenged and removed . ( September 2014 ) ( Learn how and when to remove this template message ) <\/Td> <\/Tr> <\/Table> <Table> <Tr> <Td> <\/Td> <Td> This article possibly contains original research . Please improve it by verifying the claims made and adding inline citations . Statements consisting only of original research should be removed . ( January 2015 ) ( Learn how and when to remove this template message ) <\/Td> <\/Tr> <\/Table> ( Learn how and when to remove this template message ) <\/Td> <\/Tr> <\/Table> <Table> <Tr> <Td> Part of a series on <\/Td> <\/Tr> <Tr> <Th> Internet marketing <\/Th> <\/Tr> <Tr> <Td> <Ul> <Li> Search engine optimization <\/Li> <Li> Local search engine optimisation <\/Li> <Li> Social media marketing <\/Li> <Li> Email marketing <\/Li> <Li> Referral marketing <\/Li> <Li> Content marketing <\/Li> <Li> Native advertising <\/Li> <\/Ul> <\/Td> <\/Tr> <Tr> <Th> Search engine marketing <\/Th> <\/Tr> <Tr> <Td> <Ul> <Li> Pay - per - click <\/Li> <Li> Cost per impression <\/Li> <Li> Search analytics <\/Li> <Li> Web analytics <\/Li> <\/Ul> <\/Td> <\/Tr> <Tr> <Th> Display advertising <\/Th> <\/Tr> <Tr> <Td> <Ul> <Li> Ad blocking <\/Li> <Li> Contextual advertising <\/Li> <Li> Behavioral targeting <\/Li> <\/Ul> <\/Td> <\/Tr> <Tr> <Th> Affiliate marketing <\/Th> <\/Tr> <Tr> <Td> <Ul> <Li> Cost per action <\/Li> <Li> Revenue sharing <\/Li> <\/Ul> <\/Td> <\/Tr> <Tr> <Th> Mobile advertising <\/Th> <\/Tr> <Tr> <Td> <Ul> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <\/Ul> <\/Td> <\/Tr> <\/Table> <P> Email marketing is the act of sending a commercial message , typically to a group of people , using email . In its broadest sense , every email sent to a potential or current customer could be considered email marketing . It usually involves using email to send advertisements , request business , or solicit sales or donations , and is meant to build loyalty , trust , or brand awareness . Marketing emails can be sent to a purchased lead list or a current customer database . The term usually refers to sending email messages with the purpose of enhancing a merchant 's relationship with current or previous customers , encouraging customer loyalty and repeat business , acquiring new customers or convincing current customers to purchase something immediately , and sharing third - party ads . <\/P> <P> <\/P> <H2> Contents <\/H2> ( hide ) <Ul> <Li> 1 History <\/Li> <Li> 2 Types <Ul> <Li> 2.1 Transactional emails <\/Li> <Li> 2.2 Direct emails <Ul> <Li> 2.2. 1 Mobile email marketing <\/Li> <\/Ul> <\/Li> <\/Ul> <\/Li> <Li> 3 Comparison to traditional mail <Ul> <Li> 3.1 Advantages <\/Li> <Li> 3.2 Disadvantages <\/Li> <\/Ul> <\/Li> <Li> 4 Opt - in email advertising <\/Li> <Li> 5 Legal requirements <Ul> <Li> 5.1 Australia <\/Li> <Li> 5.2 Canada <\/Li> <Li> 5.3 European Union <\/Li> <Li> 5.4 United States <\/Li> <\/Ul> <\/Li> <Li> 6 See also <\/Li> <Li> 7 References <\/Li> <\/Ul> <P> <\/P> <H2> History <\/H2> <P> Email marketing has evolved rapidly alongside the technological growth of the 21st century . Prior to this growth , when emails were novelties to the majority of customers , email marketing was not as effective . In 1978 , Gary Thuerk of Digital Equipment Corporation ( DEC ) sent out the first mass email to approximately 400 potential clients via the Advanced Research Projects Agency Network ( ARPANET ) . This email resulted in $13 million worth of sales in DEC products , and highlighted the potential of marketing through mass emails . However , as email marketing developed as an effective means of direct communication , users began blocking out content from emails with filters and blocking programs . In order to effectively communicate a message through email , marketers had to develop a way of pushing content through to the end user , without being cut out by automatic filters and spam removing software . This resulted in the birth of triggered marketing emails , which are sent to specific users based on their tracked online browsing patterns . <\/P> <P> Historically , it has been difficult to measure the effectiveness of marketing campaigns because target markets can not be adequately defined . Email marketing carries the benefit of allowing marketers to identify returns on investment and measure and improve efficiency . Email marketing allows marketers to see feedback from users in real time , and to monitor how effective their campaign is in achieving market penetration , revealing a communication channel 's scope . At the same time , however , it also means that the more personal nature of certain advertising methods , such as television advertisements , can not be captured . <\/P> <H2> Types <\/H2> <P> Email marketing can be carried out through different types of emails : <\/P> <H3> Transactional emails <\/H3> <P> Transactional emails are usually triggered based on a customer 's action with a company . To be qualified as transactional or relationship messages , these communications ' primary purpose must be `` to facilitate , complete , or confirm a commercial transaction that the recipient has previously agreed to enter into with the sender '' along with a few other narrow definitions of transactional messaging . Triggered transactional messages include dropped basket messages , password reset emails , purchase or order confirmation emails , order status emails , reorder emails , and email receipts . <\/P> <P> The primary purpose of a transactional email is to convey information regarding the action that triggered it . But , due to their high open rates ( 51.3 % compared to 36.6 % for email newsletters ) , transactional emails are an opportunity to introduce or extend the email relationship with customers or subscribers ; to anticipate and answer questions ; or to cross-sell or up - sell products or services . <\/P> <P> Many email newsletter software vendors offer transactional email support , which gives companies the ability to include promotional messages within the body of transactional emails . There are also software vendors that offer specialized transactional email marketing services , which include providing targeted and personalized transactional email messages and running specific marketing campaigns ( such as customer referral programs ) . <\/P> <H3> Direct emails <\/H3> <P> Direct email involves sending an email solely to communicate a promotional message ( for example , a special offer or a product catalog ) . Companies usually collect a list of customer or prospect email addresses to send direct promotional messages to , or they rent a list of email addresses from service companies . Safe mail marketing is also used . <\/P> Mobile email marketing <P> Email marketing develops large amounts of traffic through smartphones and tablets . Marketers are researching ways to advertise to more users and to make them view advertising for longer . However , the rate of delivery is still relatively low due to better filtering - out of advertising and users having multiple email accounts for different purposes . Because emails are generated according to the tracked behavior of consumers , it is possible to send advertising which is based on the recipient 's behavior . Because of this , modern email marketing is perceived more often as a pull strategy rather than a push strategy . <\/P> <H2> Comparison to traditional mail <\/H2> <P> There are both advantages and disadvantages to using email marketing in comparison to traditional advertising mail . <\/P> <H3> Advantages <\/H3> <P> Email marketing is popular with companies for several reasons : <\/P> <Ul> <Li> An exact return on investment can be tracked ( `` track to basket '' ) and has proven to be high when done properly . Email marketing is often reported as second only to search marketing as the most effective online marketing tactic . <\/Li> <Li> Email marketing is significantly cheaper and faster than traditional mail , mainly because of the high cost and time required in a traditional mail campaign for producing the artwork , printing , addressing , and mailing . <\/Li> <Li> Businesses and organizations who send a high volume of emails can use an ESP ( email service provider ) to gather information about the behavior of the recipients . The insights provided by consumer response to email marketing help businesses and organizations understand and make use of consumer behavior . <\/Li> <Li> Email provides a cost - effective method to test different marketing content , including visual , creative , marketing copy , and multimedia assets . The data gathered by testing in the email channel can then be used across all channels of marketing campaigns , both print and digital . <\/Li> <Li> Advertisers can reach substantial numbers of email subscribers who have opted in ( i.e. , consented ) to receive the email . <\/Li> <Li> Almost half of American Internet users check or send email on a typical day , with emails delivered between 1 am and 5 am local time outperforming those sent at other times in open and click rates . <\/Li> <Li> Email is popular with digital marketers , rising an estimated 15 % in 2009 to \u00a3 292 million in the UK . <\/Li> <Li> If compared to standard email , direct email marketing produces higher response rate and higher average order value for e-commerce businesses . <\/Li> <\/Ul> <H3> Disadvantages <\/H3> <P> As of mid-2016 email deliverability is still an issue for legitimate marketers . According to the report , legitimate email servers averaged a delivery rate of 73 % in the U.S. ; six percent were filtered as spam , and 22 % were missing . This lags behind other countries : Australia delivers at 90 % , Canada at 89 % , Britain at 88 % , France at 84 % , Germany at 80 % and Brazil at 79 % . <\/P> <P> Additionally , consumers receive on average circa 90 emails per day . <\/P> <P> Companies considering the use of an email marketing program must make sure that their program does not violate spam laws such as the United States ' Controlling the Assault of Non-Solicited Pornography and Marketing Act ( CAN - SPAM ) , the European Privacy and Electronic Communications Regulations 2003 , or their Internet service provider 's acceptable use policy . <\/P> <H2> Opt - in email advertising <\/H2> <P> Opt - in email advertising , or permission marketing , is a method of advertising via email whereby the recipient of the advertisement has consented to receive it . This method is one of several developed by marketers to eliminate the disadvantages of email marketing . <\/P> <P> Opt - in email marketing may evolve into a technology that uses a handshake protocol between the sender and receiver . This system is intended to eventually result in a high degree of satisfaction between consumers and marketers . If opt - in email advertising is used , the material that is emailed to consumers will be `` anticipated '' . It is assumed that the recipient wants to receive it , which makes it unlike unsolicited advertisements sent to the consumer . Ideally , opt - in email advertisements will be more personal and relevant to the consumer than untargeted advertisements . <\/P> <P> A common example of permission marketing is a newsletter sent to an advertising firm 's customers . Such newsletters inform customers of upcoming events or promotions , or new products . In this type of advertising , a company that wants to send a newsletter to their customers may ask them at the point of purchase if they would like to receive the newsletter . <\/P> <P> With a foundation of opted - in contact information stored in their database , marketers can send out promotional materials automatically using autoresponders -- known as drip marketing . They can also segment their promotions to specific market segments . <\/P> <H2> Legal requirements <\/H2> <H3> Australia <\/H3> <P> The Australian Spam Act 2003 is enforced by the Australian Communications and Media Authority , widely known as `` ACMA '' . The act defines the term unsolicited electronic messages , states how unsubscribe functions must work for commercial messages , and gives other key information . Fines range with 3 fines of AU $110,000 being issued to Virgin Blue Airlines ( 2011 ) , Tiger Airways Holdings Limited ( 2012 ) and Cellar master Wines Pty Limited ( 2013 ) . <\/P> <H3> Canada <\/H3> <P> The `` Canada Anti-Spam Law '' ( CASL ) went into effect on July 1 , 2014 . CASL requires an explicit or implicit opt - in from users , and the maximum fines for noncompliance are CA $ 1 million for individuals and $10 million for businesses . <\/P> <H3> European Union <\/H3> <P> In 2002 the European Union ( EU ) introduced the Directive on Privacy and Electronic Communications . Article 13 of the Directive prohibits the use of personal email addresses for marketing purposes . The Directive establishes the opt - in regime , where unsolicited emails may be sent only with prior agreement of the recipient ; this does not apply to business email addresses . <\/P> <P> The directive has since been incorporated into the laws of member states . In the UK it is covered under the Privacy and Electronic Communications ( EC Directive ) Regulations 2003 and applies to all organizations that send out marketing by some form of electronic communication . <\/P> <H3> United states <\/H3> <P> The CAN - SPAM Act of 2003 was passed by Congress as a direct response of the growing number of complaints over spam e-mails . Congress determined that the US government was showing an increased interest in the regulation of commercial electronic mail nationally , that those who send commercial e-mails should not mislead recipients over the source or content of them , and that all recipients of such emails have a right to decline them . The act authorizes a US $16,000 penalty per violation for spamming each individual recipient . However , it does not ban spam emailing outright , but imposes laws on using deceptive marketing methods through headings which are `` materially false or misleading '' . In addition there are conditions which email marketers must meet in terms of their format , their content and labeling . As a result , many commercial email marketers within the United States utilize a service or special software to ensure compliance with the act . A variety of older systems exist that do not ensure compliance with the act . To comply with the act 's regulation of commercial email , services also typically require users to authenticate their return address and include a valid physical address , provide a one - click unsubscribe feature , and prohibit importing lists of purchased addresses that may not have given valid permission . <\/P> <P> In addition to satisfying legal requirements , email service providers ( ESPs ) began to help customers establish and manage their own email marketing campaigns . The service providers supply email templates and general best practices , as well as methods for handling subscriptions and cancellations automatically . Some ESPs will provide insight and assistance with deliverability issues for major email providers . They also provide statistics pertaining to the number of messages received and opened , and whether the recipients clicked on any links within the messages . <\/P> <P> The CAN - SPAM Act was updated with some new regulations including a no - fee provision for opting out , further definition of `` sender '' , post office or private mail boxes count as a `` valid physical postal address '' and definition of `` person '' . These new provisions went into effect on July 7 , 2008 . <\/P> <H2> See also <\/H2> <Ul> <Li> CAUCE -- Coalition Against Unsolicited Commercial Email <\/Li> <Li> Customer engagement <\/Li> <Li> Suppression list <\/Li> <Li> Email spam - Unsolicited email marketing <\/Li> <\/Ul> <H2> References <\/H2> <Ol> <Li> Jump up ^ `` spam unsolicited e-mail '' . Retrieved September 19 , 2016 . <\/Li> <Li> Jump up ^ `` PUBLIC LAW 108 -- 187 -- DEC . 16 , 2003 117 STAT. 2699 '' ( PDF ) . U.S Government GPO . <\/Li> <Li> Jump up ^ ADIKESAVAN , T. MANAGEMENT INFORMATION SYSTEMS BEST PRACTICES AND APPLICATIONS IN BUSINESS . ISBN 8120348966 . Retrieved July 10 , 2015 . <\/Li> <Li> Jump up ^ MECLABS , content : MarketingSherpa , design : Scott McDaniel , code : Steve Beger , ( January 21 , 2009 ) . `` New Survey Data : Email 's ROI Makes Tactic Key for Marketers in 2009 '' . MarketingSherpa.com . Retrieved August 12 , 2017 . <\/Li> <Li> Jump up ^ Pew Internet & American Life Project , `` Tracking surveys '' , March 2000 -- March 2009 <\/Li> <Li> Jump up ^ How Scheduling Affects Rates . Mailermailer.com ( July 2012 ) . Retrieved on July 28 , 2013 . <\/Li> <Li> Jump up ^ BtoB Magazine , `` Early Email Blasts Results in Higher Click & Open Rates '' Archived 2011 - 11 - 22 at the Wayback Machine. , September 2011 <\/Li> <Li> Jump up ^ UK e-mail marketing predicted to rise 15 % . MediaWeek.co.uk ( 13 October 2009 ) <\/Li> <Li> Jump up ^ `` Why Email Marketing is King '' . Harvard Business Review ( 21 August 2012 ) <\/Li> <Li> Jump up ^ Roberts , A. `` Email deliverability is on the decline : report '' , ClickZ <\/Li> <Li> Jump up ^ Radicati , Sara . `` Email Statistics Report , 2014 - 2018 '' ( PDF ) . The Radicati Group , Inc . <\/Li> <Li> Jump up ^ `` Consumer Information '' . Consumer Information . Retrieved August 12 , 2017 . <\/Li> <Li> ^ Jump up to : Fairhead , N. ( 2003 ) `` All hail the brave new world of permission marketing via email '' ( Media 16 , August 2003 ) <\/Li> <Li> Jump up ^ Dilworth , Dianna ( 2007 ) . `` Ruth 's Chris Steak House sends sizzling e-mails for special occasions '' . DMNews . Retrieved February 19 , 2008 . <\/Li> <Li> Jump up ^ O'Brian J. & Montazemia , A. ( 2004 ) Management Information Systems ( Canada : McGraw - Hill Ryerson Ltd . ) <\/Li> <Li> Jump up ^ `` Spam : enforcement actions '' . Australian Communications and Media Authority . Australian Communications and Media Authority . Archived from the original on February 29 , 2016 . Retrieved August 15 , 2015 . <\/Li> <Li> Jump up ^ Moorcraft , Bethan . `` Law could force idle brokers back to dark ages '' . Insurance Business . Retrieved August 12 , 2017 . <\/Li> <Li> Jump up ^ `` Canada 's law on spam '' . Government of Canada . Retrieved July 19 , 2014 ... <\/Li> <Li> Jump up ^ The Privacy and Electronic Communications ( EC Directive ) Regulations 2003 Archived November 14 , 2006 , at the Wayback Machine ... Opsi.gov.uk . Retrieved on July 28 , 2013 . <\/Li> <Li> Jump up ^ `` CAN - SPAM Act : A Compliance Guide for Business '' . FTC.gov . BCP Business Center . Retrieved August 10 , 2017 . <\/Li> <Li> Jump up ^ `` FTC Approves New Rule Provision Under The CAN - SPAM Act '' . FTC.gov . June 24 , 2011 . <\/Li> <Li> Jump up ^ `` 16 CFR Part 316 Definitions and Implementation Under the CAN -- SPAM Act ; Final Rule '' ( PDF ) . FTC.gov . May 21 , 2008 . <\/Li> <\/Ol> Retrieved from `` https:\/\/en.wikipedia.org\/w\/index.php?title=Email_marketing&oldid=814071202 '' Categories : <Ul> <Li> Advertising by medium <\/Li> <Li> Email <\/Li> <Li> Digital marketing <\/Li> <Li> Market research <\/Li> <Li> Marketing techniques <\/Li> <Li> Online advertising <\/Li> <Li> Spamming <\/Li> <\/Ul> Hidden categories : <Ul> <Li> Webarchive template wayback links <\/Li> <Li> Wikipedia indefinitely semi-protected pages <\/Li> <Li> Articles needing additional references from September 2014 <\/Li> <Li> All articles needing additional references <\/Li> <Li> Articles that may contain original research from January 2015 <\/Li> <Li> All articles that may contain original research <\/Li> <Li> Articles with multiple maintenance issues <\/Li> <Li> All articles with unsourced statements <\/Li> <Li> Articles with unsourced statements from August 2017 <\/Li> <Li> Articles with unsourced statements from July 2015 <\/Li> <Li> All Wikipedia articles needing clarification <\/Li> <Li> Wikipedia articles needing clarification from August 2017 <\/Li> <Li> Articles with unsourced statements from March 2016 <\/Li> <\/Ul> <H2> <\/H2> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> Talk <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <\/Ul> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> <\/Li> <\/Ul> <H3> <\/H3> <Ul> <\/Ul> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> View source <\/Li> <Li> <\/Li> <\/Ul> <H3> <\/H3> <Ul> <\/Ul> <H3> <\/H3> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> Contents <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <\/Ul> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> About Wikipedia <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <\/Ul> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <\/Ul> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <\/Ul> <H3> <\/H3> <Ul> <Li> <\/Li> <Li> \u09ac\u09be\u0982\u09b2\u09be <\/Li> <Li> \u0411\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438 <\/Li> <Li> Catal\u00e0 <\/Li> <Li> \u010ce\u0161tina <\/Li> <Li> Espa\u00f1ol <\/Li> <Li> \u0641\u0627\u0631\u0633\u06cc <\/Li> <Li> Fran\u00e7ais <\/Li> <Li> Italiano <\/Li> <Li> \u0c95\u0ca8\u0ccd\u0ca8\u0ca1 <\/Li> <Li> \u10e5\u10d0\u10e0\u10d7\u10e3\u10da\u10d8 <\/Li> <Li> \u041c\u0430\u043a\u0435\u0434\u043e\u043d\u0441\u043a\u0438 <\/Li> <Li> Nederlands <\/Li> <Li> \u65e5\u672c \u8a9e <\/Li> <Li> Norsk <\/Li> <Li> Polski <\/Li> <Li> Portugu\u00eas <\/Li> <Li> \u0420\u0443\u0441\u0441\u043a\u0438\u0439 <\/Li> <Li> \u0421\u0440\u043f\u0441\u043a\u0438 \/ srpski <\/Li> <Li> Svenska <\/Li> <Li> \u0ba4\u0bae\u0bbf\u0bb4\u0bcd <\/Li> <Li> \u0c24\u0c46\u0c32\u0c41\u0c17\u0c41 <\/Li> <Li> \u0e44\u0e17\u0e22 <\/Li> <Li> T\u00fcrk\u00e7e <\/Li> <Li> \u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430 <\/Li> <Li> Ti\u1ebfng Vi\u1ec7t <\/Li> <Li> \u4e2d\u6587 <\/Li> 18 more <\/Ul> Edit links <Ul> <Li> This page was last edited on 6 December 2017 , at 19 : 06 . <\/Li> <Li> <\/Li> <\/Ul> <Ul> <Li> <\/Li> <Li> About Wikipedia <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <Li> <\/Li> <\/Ul> <Ul> <Li> <\/Li> <Li> <\/Li> <\/Ul>
"""

# Parse and split HTML
chunks = html_split_knowledge_graph(html_content, chunk_size=10)
# for chunk in chunks:
#     if len(chunk.split(' '))<5:
#         print(chunk)
# print("Chunks:", chunks)

# Initialize a SimpleIndexer
# indexer = SimpleIndexer()

# # Add chunks to the index
# for chunk in chunks:
#     indexer.add_document(chunk)

# # Example query
# query = "sample HTML document"
# results = indexer.search(query)

# print("Search results:", results)
