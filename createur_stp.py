from datetime import datetime
#https://en.wikipedia.org/wiki/ISO_10303-21

def creation_fichier(nom_fichier, contenue):
    f= open(nom_fichier,"w")
    f.write(contenue)
    f.close()

def date_ISO_8601():
    raw_date = str(datetime.now()).split(' ')
    ISO_date = ''.join([ raw_date[0] , 'T' , raw_date[1][:8] ])
    return ISO_date


def HEADER(nom_fichier="test",
           description="?"):
    head = ["HEADER;",
            "/* generer par un programme experimentale",
            " * pour generer des structure Voronoi solide",
            " */",
            "",
            "FILE_DESCRIPTION(",
            ''.join(["/* description */ ('",str(description),"'),"]),
            "/* implementation_level */ '2;1');",
            "",
            "FILE_NAME(",
            ''.join(["/* name */ '",str(nom_fichier),"',"]),
            ''.join(["/* time_stamp */ '",date_ISO_8601(),"',"]),
            "/* author */ ('?'),",
            "/* organization */ ('?'),",
            "/* preprocessor_version */ '?',",
            "/* originating_system */ '?',",
            "/* authorization */ '?');",
            "",
            "FILE_SCHEMA (('AUTOMOTIVE_DESIGN { 1 0 10303 214 2 1 1}'));",
            "",
            "ENDSEC;"
            ]
    str_head = '\n'.join(head)
    return str_head
    





nom_fichier = "test.stp"
contenue = ["ISO-10303-21;",
            HEADER(),
            "END-ISO-10303-21;"]
str_contenue = string = '\n'.join(contenue)
creation_fichier(nom_fichier, str_contenue)

