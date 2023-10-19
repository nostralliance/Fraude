import os, glob, shutil

from mylib import paths, functions, criterias, constants


# on récupère la liste des sociétés
societies = [society for society in os.listdir('DMR_fraude/') if os.path.isdir('DMR_fraude/' + society)]

# Pour chaque société
for society in societies:
    #stats[society]['dateferie'] += 1
    # On récupère la liste des pdfs
    pdfFiles = glob.glob(str(paths.rootPath)+'/' + str(society) + "/depot/" + "*pdf")
    #Nombre de document
    print("---Le nombre de documents pour"+" "+ str(society) +" "+ "est de:"+" "+ str(len(pdfFiles)))
    constants.STATS[society]['Nbre Total']= len(pdfFiles)
    # Pour chaque pdf récupéré
    for pdfFile in pdfFiles:
        print("Traitement de : " + pdfFile + "...")
        # On détermine le répertoire de travail
        workspace = str(paths.rootPath) + '/' + str(society)+ '/depot/TMP/'+ os.path.basename(pdfFile)
        try :
            # On génère un png pour chaque page du pdf
            pngFiles = functions.pdf2img(society, pdfFile)

            # Pour chaque png, on recherche les critères de fraude
            for pngFile in pngFiles:
                print("---Traitement de la page : " + os.path.basename(pngFile) + "...")
                # On récuprère le texte extrait du png
                pngText = functions.img2text(pngFile)
                #print(pngText)
                if "Décomptes" in pdfFile :
                    print("------Recherche d'une fausse référence d'archivage ...")
                    result = criterias.refarchivesfaux(pngText)
                    print("------Résultat de la recherche : " + str(result))

                    if result == True :
                        shutil.move(pdfFile, str(paths.rootPath) + '/' + str(society) + '/' + paths.refArchDir)
                        constants.STATS[society]['Nbre refArch'] += 1
                        break
                
                if ("Hospi" not in pdfFile):
                    print("------Recherche d'une date fériée ...")
                    result = criterias.dateferiee(pngText)
                    print("------Résultat de la recherche : "+ str(result))

                    if result == True :
                        shutil.move(pdfFile, str(paths.rootPath) + '/' + str(society) + '/' + paths.dateFerieeDir)
                        constants.STATS[society]['Nbre Dateferiee'] += 1
                        break

                print("------Recherche d'une prestation non soumise au régime obligatoire ...")
                result = criterias.rononsoumis(pngText)
                print("------Résultat de la recherche : " + str(result))

                if result == True :
                    shutil.move(pdfFile, str(paths.rootPath) + '/' + str(society) + '/' + paths.nonSoumisRoDir)
                    constants.STATS[society]['Nbre nonsoumisro'] += 1
                    break              
                
                if "Décomptes" not in pdfFile :
                    print("------Recherche d'un numéro finess suspect ...")
                    result = criterias.finessfaux(society, pngText)
                    print("------Résultat de la recherche : "+ str(result))
                    if result == True :
                        shutil.move(pdfFile, str(paths.rootPath) + '/' + str(society) + '/' + paths.finessDir)
                        constants.STATS[society]['Nbre finessfaux'] += 1
                        break
                
                print("------Recherche d'un adhérent suspect ...")
                result = criterias.adherentssuspicieux(society, pngText)
                print("------Résultat de la recherche : "+ str(result))
                
                if result == True :
                    shutil.move(pdfFile, str(paths.rootPath) + '/' + str(society) + '/' + paths.adhsusDir)
                    constants.STATS[society]['Nbre Adherent suspicieux'] += 1
                    break
                

            if result == False:
                shutil.move(pdfFile, str(paths.rootPath) + '/' + str(society) + '/' + paths.aucuneDir) 

            # On supprime les pngs dédiés à ce pdf
            shutil.rmtree(workspace)
        except Exception as e :
            print(e)
            if not os.path.exists(str(paths.rootPath) + '/' + str(society) + '/' + os.path.basename(pdfFile)):
                shutil.move(pdfFile, str(paths.rootPath) + '/' + str(society))
            else :
                os.remove(pdfFile)

print("---STATISTIQUES----")
print(constants.STATS)
