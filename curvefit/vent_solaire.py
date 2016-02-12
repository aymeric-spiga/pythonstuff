
# coding: utf-8

# ### Vent solaire (corrigé)
# 
# *Auteur: [Aymeric SPIGA](http://www.lmd.jussieu.fr/~aslmd)*
# 
# *Enoncé: Roch Smets -- Données: Gaëtan Lechat, Karine Issautier, Sylvain Beaumont*
# 
# La sonde [ULYSSE](https://fr.wikipedia.org/wiki/Ulysses_%28sonde_spatiale%29) a été lancée en 1990. Elle est la première à avoir exploré  le vent solaire au delà de 1 UA (Unité Astronomique). Ses mesures ont permis d'étudier (via les caractéristiques thermodynamiques) et de mieux comprendre la nature de son expansion dans le milieu interplanétaire. L'objet de ce problème est d'essayer de comprendre si l'expansion du vent solaire est un processus plutôt isotherme, plutôt adiabatique, ou autre. 

# Commençons par charger les données au format `ASCII` en utilisant la fonction `loadtxt`. Cette fonction est dans la librairie `numpy` que l'on doit donc importer. Par ailleurs, comme nous allons utiliser `curve_fit` et faire des figures, importons également les librairies `scipy.optimize` et `matplotlib`. 

# In[31]:

import numpy as np
import scipy.optimize as sciopt
import matplotlib.pyplot as mpl
# (ligne ci-dessous seulement pour cette page)
get_ipython().magic(u'matplotlib inline')


# Désormais, nous pouvons utiliser la fonction `loadtxt` avec l'option `unpack=True` afin de pouvoir remplir directement les trois variables d'intérêt avec le contenu du fichier `ulysse_first.txt`
# 
# * distance héliocentrique $r$ stockée en colonne 1 en unité astronomique (UA)
# * densité $\rho$ stockée en colonne 2 en cm$^{-3}$
# * pression $P$ en colonne 3 en K cm$^{-3}$

# In[32]:

dist,dens,press = np.loadtxt("ulysse_first.txt",unpack=True)


# Nous pouvons immédiatement vérifier la quantité de points collectés par ULYSSE que nous venons de charger, ainsi que, par exemple, les valeurs minimum et maximum de chacune des variables

# In[33]:

print dist.shape,dens.shape,press.shape
print dist.min(),dens.min(),press.min()
print dist.max(),dens.max(),press.max()


# Nous allons convertir la pression $P$ en megaPascal en multipliant par la constante de Boltzmann les valeurs en cm$^{-3}$

# In[34]:

import scipy.constants as scicst
press = scicst.k * press


# Nous pouvons par ailleurs faire une figure, par exemple $\rho$ en fonction de $r$. Nous allons représenter les mesures par des points rouges pour bien souligner qu'il s'agit d'une succession de mesures ponctuelles.

# In[35]:

mpl.plot(dist,dens,'r.',label="mesures ULYSSE") # commande principale
mpl.xlabel(u'distance héliocentrique(UA)') # titre axe abscisses
mpl.ylabel(u'densité (cm$^{-3}$)') # titre axe ordonnées
mpl.legend() # affichage de la légende


# Ce n'est pas par hasard que nous avons tracé $\rho$ en fonction de $r$. Nous pouvons nous demander si nous ne pouvons pas deviner physiquement comment est supposé varier $\rho$ en fonction de $r$. Si l'on raisonne sur l'expansion d'une coquille d'épaisseur $e$ infinitesimale et située à une distance $r$ du Soleil, c'est-à-dire dans un écoulement stationnaire à géométrie sphérique, le volume de la coquille est $4 \pi r^2 e$ et la densité est donc proportionnelle à $r^{-2}$. Cela est-il compatible avec les données observées par Ulysse ?
# 
# Pour le savoir, nous allons effectuer une régression d'une fonction paramétrique sur les points de données. Soit une fonction paramétrique $f_{a,b} : x \rightarrow f_{a,b}(x)$ de $x$ définie par les deux paramètres $a$ et $b$. L'exemple le plus simple est celui de la régression linéaire où $f_{a,b}(x) = a \, x + b$. Le principe de la régression est que l'on doit trouver les deux paramètres $(a_{opt},b_{opt})$ tels que les valeurs de la fonction $f_{a,b}(x_i)$ en chacune des abscisses de mesure $x_i$ soient les plus proches possibles des ordonnées de mesure $y_i$.
# 
# Traduisons cela à la situation pratique de ULYSSE. Nous disposons d'une série de mesures de distance héliocentrique $r_i$ et de densité $\rho_i$ (donc $x_i \equiv r_i$ et $y_i \equiv \rho_i$). Nous souhaitons vérifier que ces mesures suivent la loi prédite par la théorie physique $\rho = a \, r^{-2}$ avec $a$ une constante de proportionalité. La fonction de régression que nous allons choisir est donc $$ f_{a,b} : x \rightarrow a\, x^b $$ et nous souhaitons déterminer $(a_{opt},b_{opt})$ tels que les valeurs de $f_{a,b}$ prises en $r_i$ soient le plus proche possible de $\rho_i$. Si nous trouvons $b_{opt}=-2$, nous aurons validé les considérations théoriques par les observations d'Ulysse.
# 
# Commençons donc par définir ladite fonction paramétrique $f_{a,b}$ que nous appellerons en Python `regf` (pour fonction de régression).

# In[36]:

def regf(x,a,b):
    return a * (x**b)


# Pour illustrer le principe de fonction paramétrique $f_{a,b}$, dessinons `regf` pour des valeurs différentes de `a` et `b`

# In[37]:

x = np.linspace(-6,6,100)
a = 1 ; b = 2 ; mpl.plot(x,regf(x,a,b),label='$x^2$ (a=%i et b=%i)' % (a,b))
a = 3 ; b = 2 ; mpl.plot(x,regf(x,a,b),label='$3x^2$ (a=%i et b=%i)' % (a,b))
a = 1 ; b = 3 ; mpl.plot(x,regf(x,a,b),label='$x^3$ (a=%i et b=%i)' % (a,b))
mpl.legend()
mpl.xlabel('$x$') ; mpl.ylabel('$y$')


# Maintenant que $f_{a,b}$ est définie par la fonction Python `regf`, nous pouvons employer la fonction `curve_fit` qui va faire la régression dont nous parlions précédemment, c'est-à-dire nous donner les paramètres optimaux $(a_{opt},b_{opt})$ tels que les valeurs $f_{a,b}(r_i)$ soient les plus proches possibles de $\rho_i$. Cette fonction prend en argument
# 
# * la fonction paramétrique $f_{a,b}$ utilisée pour la régression
# * les abscisses de mesure $x_i$
# * les ordonnées de mesure $y_i$
# 
# et donne en sortie
# 
# * un tableau contenant les paramètres optimaux (ici au nombre de deux $a_{opt}$ et $b_{opt}$) de la fonction de régression $f_{a,b}$
# * la matrice de covariance évaluant l'optimalité des paramètres $a_{opt}$ et $b_{opt}$
# 
# L'appel à la fonction `curve_fit` s'écrit donc dans notre cas

# In[38]:

param,cov = sciopt.curve_fit(regf,dist,dens)


# Voyons les paramètres obtenus par `curve_fit`

# In[39]:

a_opt = param[0]
b_opt = param[1]
print u'résultat a=%.3f et b=%.3f' % (a_opt,b_opt)


# <small>(NB: ici il y a deux paramètres, mais il pourrait y en avoir plus en fonction de la fonction paramétrique utilisée qui pourrait être à 3,4 ... paramètres !)</small>

# Au vu du résultat obtenu pour $b$, il est clair que nous n'avons pas $\rho$ proportionnel à $r$ d'après les données ULYSSE ! Ajoutons la fonction $f_{a,b}$ pour les paramètres optimaux $a_{opt}$ et $b_{opt}$ à la figure précédemment produite avec les mesures ULYSSE

# In[40]:

mpl.plot(dist,dens,'r.',label="mesures ULYSSE") 
mpl.xlabel(u'distance héliocentrique(UA)')
mpl.ylabel(u'densité (cm$^{-3}$)')
# ajout de la fonction optimale obtenue avec curve_fit
zelab = 'curvefit $f(x) = a x^b$ avec $b=%4.2f$' % (b_opt)
mpl.plot(dist,regf(dist,a_opt,b_opt),label=zelab)
mpl.legend()


# Nous constatons que la fonction `curve_fit` a fait ce qu'elle a pu pour rapprocher le plus possible la fonction paramétrique $f_{a,b}$ des points de mesure ULYSSE, mais que le résultat n'est pas très concluant. La fonction optimale obtenue (ligne bleue) est particulièrement éloignée des mesures (ligne rouge) et ce, particulièrement à $r>1.8$ UA et $r<1.2$ UA.
# 
# Nous remarquons que pour les distances $r<1.5$ UA, plus proche du Soleil, les points de mesure sont extrêmement dispersés ce qui pourrait traduire par exemple
# 
#   1. une variabilité plus grande de la densité 
#   2. une moins bonne précision de l'instrument
# 
# Ainsi, la dispersion des mesures effectuées en $r<1.5$ UA ne paraît pas propice à vérifier une loi physique type $\rho = a r^{-2}$ obtenue par un raisonnement géométrique sur une situation moyenne.
# 
# Nous allons donc restreindre l'analyse aux données obtenues pour $r>1.5$ UA. Pour cela, il suffit d'employer la fonction `where` de `numpy` qui permet de sélectionner une partie d'un tableau vérifiant une condition particulière, pour l'utiliser ensuite pour définir un nouveau tableau.

# In[41]:

w = np.where(dist > 1.5)
dist2 = dist[w]
dens2 = dens[w]


# Nous pouvons appliquer de nouveau `curve_fit' comme précédemment. 

# In[42]:

param,cov = sciopt.curve_fit(regf,dist2,dens2)
a_opt = param[0]
b_opt = param[1]
print u'résultat a=%.3f et b=%.3f' % (a_opt,b_opt)


# Cette fois, en ayant restreint les mesures de $\rho$ au cas où $r>1.5$ UA, nous trouvons $b \simeq -2$ comme prévu théoriquement. Nous pouvons reprendre le graphique précédemment effectué pour constater cette fois la bien meilleure performance de `curvefit`.

# In[43]:

mpl.plot(dist2,dens2,'r.',label="mesures ULYSSE") 
mpl.xlabel(u'distance héliocentrique(UA)')
mpl.ylabel(u'densité (cm$^{-3}$)')
# ajout de la fonction optimale obtenue avec curve_fit
zelab = 'curvefit $f(x) = a x^b$ avec $b=%4.2f$' % (b_opt)
mpl.plot(dist2,regf(dist2,a_opt,b_opt),label=zelab)
mpl.legend()


# Considérons désormais la possibilité que l'expansion du vent solaire soit un processus isotherme. La pression $P$ et la densité $\rho$ doivent alors vérifier $ P / \rho = \alpha $ avec $\alpha$ une constante, ce qui indique que $P$ doit suivre une loi en $r^{-2}$ comme $\rho$. Vérifions cela en appliquant la même méthode que précédemment et en se restreignant au domaine $r > 1.5$ UA.

# In[44]:

press2 = press[w]
param,covp = sciopt.curve_fit(regf,dist2,press2)
a_opt = param[0]
b_opt = param[1]
print u'résultat a=%5.2e et b=%.3f' % (a_opt,b_opt)


# In[45]:

mpl.plot(dist2,press2,'r.',label="mesures ULYSSE") 
mpl.xlabel(u'distance héliocentrique(UA)')
mpl.ylabel(u'pression (MPa)')
# ajout de la fonction optimale obtenue avec curve_fit
zelab = 'curvefit $f(x) = a x^b$ avec $b=%4.2f$' % (b_opt)
mpl.plot(dist2,regf(dist2,a_opt,b_opt),label=zelab)
mpl.legend()


# Le recours à `curve_fit` semble fonctionner correctement, avec une fonction obtenue qui approche raisonnablement la tendance dessinée par les mesures (impression visuelle qu'il s'agirait de confirmer en étudiant plus précisément les sorties de `curve_fit`, ce que nous ne ferons pas ici). Nous trouvons que $b = -2.5$, ce qui nous indique une loi en $r^{-5/2}$ pour $P$ et non une loi en $r^{-2}$. Nous concluons que l'expansion du vent solaire n'est pas un processus isotherme, même si elle s'en rapproche.
# 
# Pour une expansion adiabatique, la pression devrait évoluer comme $n^{\gamma}$, soit $r^{-2 \gamma} = r^{-10/3}$. C'est encore moins le cas. L'expansion du vent solaire n'est donc pour sûr pas adiabatique. Il faut donc identifier la source du chauffage du vent solaire... ce qui est encore un sujet de recherche active !
