"""
Trusted opportunity sources for scholarships, fellowships, and accelerators
"""

OPPORTUNITY_SOURCES = {
    "scholarships": [
        {
            "name": "Partiu Intercambio",
            "base_url": "https://partiuintercambio.org",
            "search_url": "https://partiuintercambio.org/bolsas-de-estudo/",
            "selectors": {
                "container": ".scholarship-item, .bolsa-item",
                "title": "h3, .title, .scholarship-title",
                "organization": ".organization, .instituicao",
                "amount": ".amount, .valor",
                "deadline": ".deadline, .prazo",
                "url": "a"
            }
        },
        {
            "name": "WeMakeScholars",
            "base_url": "https://www.wemakescholars.com",
            "search_url": "https://www.wemakescholars.com/scholarship",
            "selectors": {
                "container": ".scholarship-card, .scholarship-item",
                "title": ".scholarship-title, h3",
                "organization": ".scholarship-provider, .university",
                "amount": ".scholarship-amount, .amount",
                "deadline": ".scholarship-deadline, .deadline",
                "url": ".scholarship-title a, h3 a"
            }
        },
        {
            "name": "Fulbright Brazil",
            "base_url": "https://fulbright.org.br",
            "search_url": "https://fulbright.org.br/bolsas-para-brasileiros/",
            "selectors": {
                "container": ".scholarship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "Fulbright",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        },
        {
            "name": "Fulbright US",
            "base_url": "https://fulbright.org.br",
            "search_url": "https://fulbright.org.br/awards-for-us-citizens/",
            "selectors": {
                "container": ".scholarship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "Fulbright",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        }
    ],
    "fellowships": [
        {
            "name": "ProFellow",
            "base_url": "https://www.profellow.com",
            "search_url": "https://www.profellow.com/open-calls/",
            "selectors": {
                "container": ".fellowship-item, .opportunity-item",
                "title": "h3, .fellowship-title",
                "organization": ".organization, .provider",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .fellowship-title a"
            }
        },
        {
            "name": "Opportunities for Youth",
            "base_url": "https://opportunitiesforyouth.org",
            "search_url": "https://opportunitiesforyouth.org/",
            "selectors": {
                "container": ".opportunity-item, .fellowship-card",
                "title": "h3, .opportunity-title",
                "organization": ".organization, .provider",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .opportunity-title a"
            }
        },
        {
            "name": "Audacious Project",
            "base_url": "https://www.audaciousproject.org",
            "search_url": "https://www.audaciousproject.org/apply",
            "selectors": {
                "container": ".fellowship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "Audacious Project",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        },
        {
            "name": "Start Fellowship",
            "base_url": "https://www.startglobal.org",
            "search_url": "https://www.startglobal.org/start-fellowship",
            "selectors": {
                "container": ".fellowship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "Start Global",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        },
        {
            "name": "Westerwelle Foundation",
            "base_url": "https://westerwelle-foundation.com",
            "search_url": "https://westerwelle-foundation.com/programs/young-founders-program/",
            "selectors": {
                "container": ".fellowship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "Westerwelle Foundation",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        },
        {
            "name": "Watson Impact Fellowships",
            "base_url": "https://watson.is",
            "search_url": "https://watson.is/impact-fellowships/",
            "selectors": {
                "container": ".fellowship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "Watson Institute",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        },
        {
            "name": "Kauffman Fellows",
            "base_url": "https://www.kauffmanfellows.org",
            "search_url": "https://www.kauffmanfellows.org/",
            "selectors": {
                "container": ".fellowship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "Kauffman Fellows",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        },
        {
            "name": "ChangeMakerXchange",
            "base_url": "https://changemakerxchange.org",
            "search_url": "https://changemakerxchange.org/ai/",
            "selectors": {
                "container": ".fellowship-item, .program-item",
                "title": "h3, .program-title",
                "organization": "ChangeMakerXchange",
                "deadline": ".deadline, .application-deadline",
                "url": "a"
            }
        }
    ],
    "accelerators": [
        {
            "name": "YouNoodle",
            "base_url": "https://platform.younoodle.com",
            "search_url": "https://platform.younoodle.com/competition/apply",
            "selectors": {
                "container": ".competition-item, .program-card",
                "title": "h3, .competition-title",
                "organization": ".organization, .host",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .competition-title a"
            }
        },
        {
            "name": "OpportunityDesk",
            "base_url": "https://opportunitydesk.org",
            "search_url": "https://opportunitydesk.org/",
            "selectors": {
                "container": ".opportunity-item, .program-card",
                "title": "h3, .opportunity-title",
                "organization": ".organization, .provider",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .opportunity-title a"
            }
        },
        {
            "name": "F6S Programs",
            "base_url": "https://www.f6s.com",
            "search_url": "https://www.f6s.com/programs",
            "selectors": {
                "container": ".program-card, .accelerator-item",
                "title": "h3, .program-title",
                "organization": ".organization, .company",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "SEBRAE Startups",
            "base_url": "https://programas.sebraestartups.com.br",
            "search_url": "https://programas.sebraestartups.com.br/programas",
            "selectors": {
                "container": ".program-item, .accelerator-card",
                "title": "h3, .program-title",
                "organization": "SEBRAE",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "Station F",
            "base_url": "https://stationf.co",
            "search_url": "https://stationf.co/programs",
            "selectors": {
                "container": ".program-item, .accelerator-card",
                "title": "h3, .program-title",
                "organization": "Station F",
                "location": "Paris, France",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "Emerge Americas",
            "base_url": "https://emergeamericas.com",
            "search_url": "https://emergeamericas.com/programs/",
            "selectors": {
                "container": ".program-item, .accelerator-card",
                "title": "h3, .program-title",
                "organization": "Emerge Americas",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "Startup World Cup",
            "base_url": "https://www.startupworldcup.io",
            "search_url": "https://www.startupworldcup.io/",
            "selectors": {
                "container": ".competition-item, .program-card",
                "title": "h3, .competition-title",
                "organization": "Startup World Cup",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .competition-title a"
            }
        },
        {
            "name": "Global Startup Awards",
            "base_url": "https://www.globalstartupawards.com",
            "search_url": "https://www.globalstartupawards.com/",
            "selectors": {
                "container": ".award-item, .program-card",
                "title": "h3, .award-title",
                "organization": "Global Startup Awards",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .award-title a"
            }
        },
        {
            "name": "Web Summit",
            "base_url": "https://websummit.com",
            "search_url": "https://websummit.com/startups/",
            "selectors": {
                "container": ".startup-item, .program-card",
                "title": "h3, .startup-title",
                "organization": "Web Summit",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .startup-title a"
            }
        },
        {
            "name": "TechCrunch Disrupt",
            "base_url": "https://techcrunch.com",
            "search_url": "https://techcrunch.com/events/tc-disrupt-2025/",
            "selectors": {
                "container": ".event-item, .program-card",
                "title": "h3, .event-title",
                "organization": "TechCrunch",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .event-title a"
            }
        },
        {
            "name": "BRICS Women Startups",
            "base_url": "https://bricswomen.com",
            "search_url": "https://bricswomen.com/pt/brics-womensstartups-contest/",
            "selectors": {
                "container": ".contest-item, .program-card",
                "title": "h3, .contest-title",
                "organization": "BRICS Women",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .contest-title a"
            }
        },
        {
            "name": "NextStep Accelerator",
            "base_url": "https://nextstepaccelerator.com",
            "search_url": "https://nextstepaccelerator.com/investment/",
            "selectors": {
                "container": ".accelerator-item, .program-card",
                "title": "h3, .accelerator-title",
                "organization": "NextStep Accelerator",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .accelerator-title a"
            }
        },
        {
            "name": "Decelera Ventures",
            "base_url": "https://www.decelera.ventures",
            "search_url": "https://www.decelera.ventures/",
            "selectors": {
                "container": ".program-item, .accelerator-card",
                "title": "h3, .program-title",
                "organization": "Decelera Ventures",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "Ventiur",
            "base_url": "https://ventiur.net",
            "search_url": "https://ventiur.net/",
            "selectors": {
                "container": ".program-item, .accelerator-card",
                "title": "h3, .program-title",
                "organization": "Ventiur",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "776 Foundation",
            "base_url": "https://www.776.org",
            "search_url": "https://www.776.org/",
            "selectors": {
                "container": ".program-item, .accelerator-card",
                "title": "h3, .program-title",
                "organization": "776 Foundation",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "500 Global",
            "base_url": "https://flagship.aplica.500.co",
            "search_url": "https://flagship.aplica.500.co/",
            "selectors": {
                "container": ".program-item, .accelerator-card",
                "title": "h3, .program-title",
                "organization": "500 Global",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .program-title a"
            }
        },
        {
            "name": "Techstars",
            "base_url": "https://www.techstars.com",
            "search_url": "https://www.techstars.com/accelerators",
            "selectors": {
                "container": ".accelerator-item, .program-card",
                "title": "h3, .accelerator-title",
                "organization": "Techstars",
                "location": ".location, .region",
                "deadline": ".deadline, .application-deadline",
                "url": "h3 a, .accelerator-title a"
            }
        }
    ]
}

# Additional trusted sources
ADDITIONAL_SOURCES = [
    {
        "name": "Idealist",
        "base_url": "https://www.idealist.org",
        "search_url": "https://www.idealist.org/en/fellowships",
        "type": "fellowships",
        "selectors": {
            "container": ".opportunity-card",
            "title": ".opportunity-title",
            "organization": ".opportunity-organization",
            "location": ".opportunity-location",
            "deadline": ".opportunity-deadline",
            "url": ".opportunity-title a"
        }
    },
    {
        "name": "UN Opportunities",
        "base_url": "https://careers.un.org",
        "search_url": "https://careers.un.org/lbw/Home.aspx",
        "type": "fellowships",
        "selectors": {
            "container": ".job-listing",
            "title": ".job-title",
            "organization": ".job-organization",
            "location": ".job-location",
            "deadline": ".job-deadline",
            "url": ".job-title a"
        }
    }
]
