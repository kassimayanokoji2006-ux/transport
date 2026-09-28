from django.db import models



class Etudiant(models.Model):
    matrE = models.CharField(max_length=20, primary_key=True)  
    nomE = models.CharField(max_length=50)
    prenomE = models.CharField(max_length=50)
    dateN = models.DateField()
    adresse = models.CharField(max_length=255)
    telParent = models.CharField(max_length=15)



class Bus(models.Model):
    idBus = models.CharField(max_length=20, primary_key=True)  
    matrV = models.CharField(max_length=20)
    marque = models.CharField(max_length=50)
    capacite = models.IntegerField()



class Trans(models.Model):
    refT = models.CharField(max_length=20, primary_key=True) 
    dateTrans = models.DateField()
    matrE = models.ForeignKey('Etudiant', on_delete=models.CASCADE)  
    idBus = models.ForeignKey('Bus', on_delete=models.CASCADE)      
