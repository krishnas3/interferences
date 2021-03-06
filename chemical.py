from pydpi.drug import constitution, topology, connectivity, kappa, bcut, basak, estate, moran, moreaubroto, geary, \
    charge, molproperty, moe, fingerprint
from pydpi import pydrug
from molvs import standardize_smiles, Standardizer


from rdkit.Chem.SaltRemover import SaltRemover
from rdkit import Chem

from copy import deepcopy
from os import path, getcwd, remove, system, listdir

import toolbox
import pathFolder
import runExternalSoft



LSALTDEF="[Cl,Br,I]\n[Li,Na,K,Ca,Mg]\n[O,N]\n[N](=O)(O)O\n[P](=O)(O)(O)O\n[P](F)(F)(F)(F)(F)F\n[S](=O)(=O)(O)O\n[CH3][S](=O)(=O)(O)\nc1cc([CH3])ccc1[S](=O)(=O)(O)\n[CH3]C(=O)O\nFC(F)(F)C(=O)O\nOC(=O)C=CC(=O)O\nOC(=O)C(=O)O\nOC(=O)C(O)C(O)C(=O)O\nC1CCCCC1[NH]C1CCCCC1\n"
LSALT="[Co]"


LSMILESREMOVE=["[C-]#N", "[Al+3]", "[Gd+3]", "[Pt+2]", "[Au+3]", "[Bi+3]", "[Al]", "[Si+4]", "[Fe]", "[Zn]", "[Fe+2]",
               "[Ru+8]", "[Fe+]", "[Sr++]", "[Fe+3]", "[O--]", "[OH-]", "[Mn++]", "[La+3]", "[Lu+3]", "[SH-]", "[Pt+4]",
               "[Fe++]", "[W]", "[Cu+2]", "[Cr+3]", "[Tc+7]", "[Xe]", "[Tl+]", "[Zn+2]", "[F-]", "[C]", "[He]", "N#N",
               "O=O", "Cl[Ra]Cl", "[Mn+2]", "N#[N+][O-]", "II", "[Ga+3]", "[Mo+10]", "[Zn]", "[Fe]", "[Si+4]", "[Al]",
               "[B+3]"]


LKAPA = ['kappa1', 'kappa2', 'kappa3', 'kappam1', 'kappam2', 'kappam3', 'phi']
LBUCUT =["bcutp16","bcutp15","bcutp14","bcutp13","bcutp12","bcutp11","bcutp10",
        "bcutp9","bcutp8","bcutp7","bcutp6","bcutp5","bcutp4","bcutp3",
        "bcutp2","bcutp1"]
LESTATE = ['Smax38', 'Smax39', 'Smax34', 'Smax35', 'Smax36', 'S43', 'Smax30', 'Smax31', 'Smax32', 'Smax33', 'S57',
           'S56', 'S55', 'S54', 'S53', 'S52', 'S51', 'S50', 'Smin49', 'S59', 'S58', 'Smin69', 'Smin68', 'Smin27',
           'Sfinger30', 'Sfinger31', 'Sfinger32', 'Sfinger33', 'Sfinger34', 'Sfinger35', 'Sfinger36', 'Sfinger37',
           'Sfinger38', 'Sfinger39', 'Smax2', 'Smax3', 'Smax4', 'Smax5', 'Smax6', 'Smax7', 'Smin77', 'Smax29', 'Smax37',
           'Smax23', 'Smax22', 'Smax21', 'Smax20', 'Smax27', 'Smax26', 'Smax25', 'Smax24', 'S44', 'S45', 'S46', 'S47',
           'S40', 'S41', 'S42', 'S17', 'Smin44', 'S48', 'S49', 'Smin8', 'Smin29', 'Smin28', 'Sfinger45', 'Sfinger44',
           'Sfinger47', 'Sfinger46', 'Sfinger41', 'Sfinger40', 'Sfinger43', 'Sfinger42', 'Smax47', 'Smin73', 'Smin70',
           'Smin71', 'Sfinger49', 'Sfinger48', 'Smin74', 'Smin75', 'Smin67', 'Smin6', 'Smin9', 'Smin7', 'Smin47',
           'Smax41', 'S79', 'S78', 'Smin19', 'Smax58', 'Smax59', 'S71', 'S70', 'S73', 'S72', 'S75', 'S74', 'S77',
           'S76', 'Smax73', 'Smin78', 'Sfinger56', 'Sfinger57', 'Sfinger54', 'Sfinger55', 'Sfinger52', 'Sfinger53',
           'Sfinger50', 'Sfinger51', 'Smin61', 'Smin60', 'Smin63', 'Smin62', 'Smin65', 'Smin64', 'Sfinger58',
           'Sfinger59', 'Smin48', 'Smin42', 'Smin76', 'Smin41', 'Smin72', 'Smax40', 'Smin40', 'Smax49', 'Smax48',
           'S68', 'S69', 'S66', 'S67', 'S64', 'S65', 'S62', 'S63', 'S60', 'S61', 'Smin54', 'Smax52', 'Sfinger69',
           'Sfinger68', 'Smin50', 'Smin51', 'Smin52', 'Smin53', 'Sfinger63', 'Sfinger62', 'Sfinger61', 'Sfinger60',
           'Sfinger67', 'S10', 'Sfinger65', 'Sfinger64', 'S13', 'S12', 'Sfinger76', 'Smin56', 'S9', 'S8', 'S3', 'S2',
           'S1', 'Smin55', 'S7', 'S6', 'S5', 'S4', 'Smax78', 'Smax45', 'Smax11', 'Sfinger72', 'Smin66', 'Smax44',
           'Smax70', 'Smax71', 'Smax72', 'S14', 'Smax74', 'Smax75', 'Smax76', 'Smax77', 'Smin43', 'Smax8', 'S19',
           'S18', 'Sfinger78', 'Sfinger79', 'Smin45', 'Smax9', 'Sfinger74', 'Sfinger75', 'S11', 'Sfinger77',
           'Sfinger70', 'Sfinger71', 'S15', 'Sfinger73', 'Smax43', 'Smin16', 'Smax42', 'Smax53', 'Smax66', 'Smax65',
           'Smax64', 'Smax63', 'Smax62', 'Smax61', 'Smax60', 'Smin26', 'Smax69', 'Smax68', 'Smax0', 'Smin57', 'Smax1',
           'Smin17', 'Smin36', 'Smin37', 'Smin34', 'Smin35', 'Smin32', 'Smin33', 'Smin30', 'Smin31', 'Smax67', 'Smin46',
           'Smax51', 'Smin38', 'Smin39', 'Smax12', 'Smax13', 'Smax10', 'S16', 'Smax16', 'Smax17', 'Smax14', 'Smax15',
           'Smin20', 'Smax18', 'Smax19', 'Sfinger66', 'Smax56', 'Smax28', 'Smax57', 'Smax54', 'Smin58', 'Smax55', 'S39',
           'S38', 'Smax46', 'S35', 'S34', 'S37', 'S36', 'S31', 'S30', 'S33', 'S32', 'Smin25', 'Smin24', 'Sfinger18',
           'Sfinger19', 'Smin21', 'Smax50', 'Smin23', 'Smin22', 'Sfinger12', 'Sfinger13', 'Sfinger10', 'Sfinger11',
           'Sfinger16', 'Sfinger17', 'Sfinger14', 'Sfinger15', 'Sfinger8', 'Sfinger9', 'Smin4', 'Smin5', 'Smin2',
           'Smin3', 'Smin0', 'Smin1', 'Sfinger1', 'Sfinger2', 'Sfinger3', 'Sfinger4', 'Sfinger5', 'Sfinger6',
           'Sfinger7', 'S22', 'S23', 'S20', 'S21', 'S26', 'S27', 'S24', 'S25', 'Smin59', 'S28', 'S29', 'Smin18',
           'Smin10', 'Smin11', 'Smin12', 'Smin13', 'Smin14', 'Smin15', 'Sfinger29', 'Sfinger28', 'Sfinger27',
           'Sfinger26', 'Sfinger25', 'Sfinger24', 'Sfinger23', 'Sfinger22', 'Sfinger21', 'Sfinger20']
LMOREAUBROTO = ['ATSe1', 'ATSe2', 'ATSe3', 'ATSe4', 'ATSe5', 'ATSe6', 'ATSe7', 'ATSe8', 'ATSp8', 'ATSp3', 'ATSv8',
                'ATSp1', 'ATSp7', 'ATSp6', 'ATSp5', 'ATSp4', 'ATSv1', 'ATSp2', 'ATSv3', 'ATSv2', 'ATSv5', 'ATSv4',
                'ATSv7', 'ATSv6', 'ATSm8', 'ATSm1', 'ATSm2', 'ATSm3', 'ATSm4', 'ATSm5', 'ATSm6', 'ATSm7']
LMORAN = ['MATSv8', 'MATSp4', 'MATSp8', 'MATSv1', 'MATSp6', 'MATSv3', 'MATSv2', 'MATSv5', 'MATSv4', 'MATSv7', 'MATSv6',
          'MATSm8', 'MATSp1', 'MATSm4', 'MATSm5', 'MATSm6', 'MATSm7', 'MATSm1', 'MATSm2', 'MATSm3', 'MATSe4', 'MATSe5',
          'MATSe6', 'MATSe7', 'MATSe1', 'MATSe2', 'MATSe3', 'MATSe8', 'MATSp3', 'MATSp7', 'MATSp5', 'MATSp2']
LGEARY = ['GATSp8', 'GATSv3', 'GATSv2', 'GATSv1', 'GATSp6', 'GATSv7', 'GATSv6', 'GATSv5', 'GATSv4', 'GATSe2', 'GATSe3',
          'GATSv8', 'GATSe6', 'GATSe7', 'GATSe4', 'GATSe5', 'GATSp5', 'GATSp4', 'GATSp7', 'GATSe1', 'GATSp1', 'GATSp3',
          'GATSp2', 'GATSe8', 'GATSm2', 'GATSm3', 'GATSm1', 'GATSm6', 'GATSm7', 'GATSm4', 'GATSm5', 'GATSm8']
LMOE = ['EstateVSA8', 'EstateVSA9', 'EstateVSA4', 'EstateVSA5', 'EstateVSA6', 'EstateVSA7', 'EstateVSA0', 'EstateVSA1',
        'EstateVSA2', 'EstateVSA3', 'PEOEVSA13', 'PEOEVSA12', 'PEOEVSA11', 'PEOEVSA10', 'MTPSA', 'VSAEstate0',
        'VSAEstate1', 'VSAEstate2', 'VSAEstate3', 'VSAEstate4', 'VSAEstate5', 'VSAEstate6', 'VSAEstate7', 'VSAEstate8',
        'LabuteASA', 'PEOEVSA3', 'PEOEVSA2', 'PEOEVSA1', 'PEOEVSA0', 'PEOEVSA7', 'PEOEVSA6', 'PEOEVSA5', 'PEOEVSA4',
        'MRVSA5', 'MRVSA4', 'PEOEVSA9', 'PEOEVSA8', 'MRVSA1', 'MRVSA0', 'MRVSA3', 'MRVSA2', 'MRVSA9', 'slogPVSA10',
        'slogPVSA11', 'MRVSA8', 'MRVSA7', 'MRVSA6', 'EstateVSA10', 'slogPVSA2', 'slogPVSA3', 'slogPVSA0', 'slogPVSA1',
        'slogPVSA6', 'slogPVSA7', 'slogPVSA4', 'slogPVSA5', 'slogPVSA8', 'slogPVSA9', 'VSAEstate9', 'VSAEstate10']

LOPERA = ["MolWeight", "nbAtoms", "nbHeavyAtoms", "nbC", "nbO", "nbH", "nbAromAtom", "nbRing", "nbHeteroRing",
          "Sp3Sp2HybRatio", "nbRotBd", "nbHBdAcc", "ndHBdDon", "nbLipinskiFailures", "TopoPolSurfAir", "MolarRefract",
          "CombDipolPolariz", "LogBCF_pred", "BP_pred", "LogP_pred", "MP_pred", "LogVP_pred", "LogWS_pred", "LogOH_pred",
          "BioDeg_LogHalfLife_pred", "LogHL_pred", "LogKM_pred", "LogKOA_pred", "LogKoc_pred", "RT_pred",
          "Sim_index_BP", "Sim_index_LogP", "Sim_index_VP", "Sim_index_AOH", "Sim_index_BioDeg", "Sim_index_ReadyBiodeg",
          "Sim_index_KM", "Sim_index_KOA", "Sim_index_RT"]#, "pka_acid", "pka_basic"]

def transformOPERAList(ddesc):

    for chem in ddesc.keys():
        ldel = []
        for desc in ddesc[chem].keys():
            if desc == "MW":
                new = "MolWeight"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "nAtom":
                new = "nbAtoms"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)

            if desc == "nHeavyAtom":
                new = "nbHeavyAtoms"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "nC":
                new = "nbC"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)

            if desc == "nO":
                new = "nbO"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "nH":
                new = "nbH"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)

            if desc == "naAromAtom":
                new = "nbAromAtom"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "nRing":
                new = "nbRing"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)

            if desc == "nHeteroRing":
                new = "nbHeteroRing"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "HybRatio":
                new = "Sp3Sp2HybRatio"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)

            if desc == "nRotB":
                new = "nbRotBd"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "nHBAcc":
                new = "nbHBdAcc"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)

            if desc == "nHBDon":
                new = "ndHBdDon"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "LipinskiFailures":
                new = "nbLipinskiFailures"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)

            if desc == "TopoPSA":
                new = "TopoPolSurfAir"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "AMR":
                new = "MolarRefract"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)


            elif desc == "MLFER_S":
                new = "CombDipolPolariz"
                ddesc[chem][new] = ddesc[chem][desc]
                ldel.append(desc)



        for deldesc in ldel:
            del ddesc[chem][deldesc]




LMOLPROP = ['LogP', 'LogP2', 'MR', 'TPSA', 'Hy', 'UI']
LMOLPROP = ['LogP2', 'TPSA', 'Hy', 'UI']# remove duplicate from opera

loader = pydrug.PyDrug()




def normalize(mol, lout):
    s = Standardizer()
    molstandardized = s.standardize(mol)
    #print molstandardized
    lout.append(molstandardized)



def getLdesc (typeDesc, RKitPhyco=1):

    lout = []
    if typeDesc == "1D2D" and RKitPhyco == 1:
        # listdesc
        lout = lout + constitution._constitutional.keys() + ["nheavy"] + LMOLPROP + topology._Topology.keys() + \
               connectivity._connectivity.keys() + LKAPA + LBUCUT + basak._basak.keys() + LESTATE + LMOREAUBROTO + \
               LMORAN + LGEARY + charge._Charge.keys() + LMOE

    elif typeDesc == "1D2D" and RKitPhyco == 0:
        # listdesc
        lout = lout + constitution._constitutional.keys() + ["nheavy"] + topology._Topology.keys() + \
               connectivity._connectivity.keys() + LKAPA + LBUCUT + basak._basak.keys() + LESTATE + LMOREAUBROTO + \
               LMORAN + LGEARY + charge._Charge.keys() + LMOE

    if typeDesc == "Opera":
        lout = LOPERA

    return lout



class chemical:

    def __init__(self, name, smiles, psdf=""):

        self.name = name
        self.smi = smiles
        self.psdf = psdf
        self.log = "Init => " + str(smiles) + "\n"

        # generate smi?

        #smile = runExternalSoft.babelConvertSDFtoSMILE(self.compound["sdf"])
        #self.compound["SMILES"] = smile
            # print smile
        #except:


    def prepareChem(self, prSMIclean):


        psmiclean = prSMIclean + self.name + ".smi"

        # try if existing
        if path.exists(psmiclean):
            psmiclean = prSMIclean + self.name + ".smi"
            fsmiclean = open(psmiclean, "r")
            smiclean = fsmiclean.readlines()
            fsmiclean.close()

            smiclean = smiclean[0].strip()
            self.smiclean = smiclean
            self.mol = Chem.MolFromSmiles(smiclean)
            self.log = self.log + "Prep SMI :" + str(self.smi) + "\n"
            self.log = self.log + "Prepared SMI :" + str(self.smiclean) + "\n"

        else:
            #self.mol = loader.ReadMolFromSmile(self.smi)

            s = Standardizer()
            mol = Chem.MolFromSmiles(self.smi)

            try:
                out = toolbox.timeFunction(normalize, mol)
                if out == "ERROR":
                    self.log = self.log + "Normalize SMILES: ERROR DURING THE PROCESS\n"
                else:
                    molstandardized = out
            except:
                self.log = self.log + "Normalize SMILES: ERROR INPUT SMI\n"


            if "molstandardized" in locals():

                smilestandadized = Chem.MolToSmiles(molstandardized)

                # remove salt
                # 1.default
                remover = SaltRemover(defnFilename="Salts.txt")
                mol = Chem.MolFromSmiles(smilestandadized)
                molcleandefault = remover(mol)
                # 2. Personal remover
                homeremover = SaltRemover(defnData=LSALT)
                molclean = homeremover(molcleandefault)
                smilesclean = Chem.MolToSmiles(molclean)
                # 3. SMILES remove other manual salts + fragments -> for fragment take one if exactly same compound
                lelem = smilesclean.split(".")
                if len(lelem) > 1:
                    # reduce double, case of several salts are included - 255
                    lelem = list(set(lelem))
                    for smilesdel in LSMILESREMOVE:
                        if smilesdel in lelem:
                            lelem.remove(smilesdel)
                    try:
                        lelem.remove("")  # case of bad smile
                    except:
                        pass
                    if len(lelem) == 1:
                        smilesclean = str(lelem[0])
                    else:
                        # 4. Fragments
                        # Case of fragment -> stock in log file, check after to control
                        self.log = self.log + "Fragments after standardization: " + smilesclean + "\n"
                        smilesclean = ""

                if smilesclean == "":
                    self.log = self.log + "ERROR SMILES: SMILES empty after preparation\n"

                else:
                    self.log = self.log + "Prepared SMI :" + str(smilesclean) + "\n"

                    fsmiclean = open(psmiclean, "w")
                    fsmiclean.write(smilesclean)
                    fsmiclean.close()

                    self.smiclean = smilesclean
                    self.psmiclean = psmiclean


    def compute1D2DDesc(self, prDescbyChem):

        self.prDesc = prDescbyChem
        # check if descriptors already computed
        pdes = prDescbyChem + self.name + ".txt"
        if path.exists(pdes) and path.getsize(pdes) > 10:
            filin = open(pdes, "r")
            llines = filin.readlines()
            filin.close()
            ldesc = llines[0].strip().split("\t")[1:]
            lval = llines[1].strip().split("\t")[1:]
            ddes = {}
            i = 0
            while i < len(ldesc):
                ddes[ldesc[i]] = lval[i]
                i += 1
            self.allDesc = ddes
            self.log = self.log + "Desc already computed -> " + pdes + "\n"
            return 0

        if not "smiclean" in self.__dict__:
            self.log = self.log + "No smiles prepared\n"
            return 1
        else:
            self.mol = loader.ReadMolFromSmile(self.smiclean)
            print self.smiclean

            try:
                self.consti = constitution.GetConstitutional(self.mol)
            except:
                self.consti = {}
            self.compo = {}
            try:
                self.compo["nheavy"] = self.mol.GetNumHeavyAtoms()
            except:
                self.compo = {}

            try:
                self.molprop = molproperty.GetMolecularProperty(self.mol)
            except:
                self.molprop = {}

                # 2D
            try:
                self.topo = topology.GetTopology(self.mol)
            except:
                self.topo = {}
            try:
                self.connect = connectivity.GetConnectivity(self.mol)
            except:
                self.connect = {}
            try:
                self.kap = kappa.GetKappa(self.mol)
            except:
                self.kap = {}
            try:
                self.burden = bcut.GetBurden(self.mol)
            except:
                self.burden = {}
            try:
                self.basakD = basak.Getbasak(self.mol)
            except:
                self.basakD = {}
            try:
                self.est = estate.GetEstate(self.mol)
            except:
                self.est = {}
            try:
                self.moreauBurto = moreaubroto.GetMoreauBrotoAuto(self.mol)
            except:
                self.moreauBurto = {}
            try:
                self.autcormoran = moran.GetMoranAuto(self.mol)
            except:
                self.autcormoran = {}
            try:
                self.gearycor = geary.GetGearyAuto(self.mol)
            except:
                self.gearycor = {}
            try:
                self.charges = charge.GetCharge(self.mol)
            except:
                self.charges = {}
            try:
                self.MOE = moe.GetMOE(self.mol)
            except:
                self.MOE = {}

            # combine all 1D2D
            if not "allDesc" in dir(self):
                self.allDesc = dict()
            self.allDesc.update(deepcopy(self.consti))
            self.allDesc.update(deepcopy(self.compo))
            self.allDesc.update(deepcopy(self.molprop))
            self.allDesc.update(deepcopy(self.topo))
            self.allDesc.update(deepcopy(self.connect))
            self.allDesc.update(deepcopy(self.kap))
            self.allDesc.update(deepcopy(self.burden))
            self.allDesc.update(deepcopy(self.basakD))
            self.allDesc.update(deepcopy(self.est))
            self.allDesc.update(deepcopy(self.moreauBurto))
            self.allDesc.update(deepcopy(self.autcormoran))
            self.allDesc.update(deepcopy(self.gearycor))
            self.allDesc.update(deepcopy(self.charges))
            self.allDesc.update(deepcopy(self.MOE))
            if self.allDesc == {}:
                return 1
            else:
                return 0




    def computeOpera(self, update):

        if "opera" in self.__dict__:
            return 1
        else:
            # check if descriptors already computed
            pdes = self.prDesc + self.name + ".txt"
            if path.exists(pdes) and path.getsize(pdes) > 10 and update == 0:
                filin = open(pdes, "r")
                llines = filin.readlines()
                filin.close()
                ldesc = llines[0].strip().split("\t")[1:]
                lval = llines[1].strip().split("\t")[1:]
                ddes = {}
                i = 0
                while i < len(ldesc):
                    ddes[ldesc[i]] = lval[i]
                    i += 1
                self.allDesc = ddes
                self.log = self.log + "Desc already computed -> " + pdes + "\n"
                return 0

            dopera = {}

            prOPERA = pathFolder.createFolder(self.prDesc + "OPERA/" + self.name + "/")
            molH = Chem.AddHs(self.mol)

            psdf = prOPERA + str(self.name) + ".sdf"
            filsdf = open(psdf, "w")
            filsdf.write(Chem.MolToMolBlock(molH))
            filsdf.close()

            pdesc2D = runExternalSoft.runPadel(prOPERA)

            ddesc2D = toolbox.loadMatrix(pdesc2D, sep = ",")
            transformOPERAList(ddesc2D)
            for desc2D in ddesc2D[ddesc2D.keys()[0]].keys():
                if desc2D in LOPERA:
                    dopera[desc2D] = ddesc2D[ddesc2D.keys()[0]][desc2D]

            lpdesc = runExternalSoft.runOPERA(psdf, pdesc2D, prOPERA)

            for pdesc in lpdesc:
                try:ddesc = toolbox.loadMatrix(pdesc, ",")
                except:
                    print pdesc
                    dddd
                for desc in ddesc[ddesc.keys()[0]].keys():
                    if desc in LOPERA:
                        dopera[desc] = ddesc[ddesc.keys()[0]][desc]

            self.opera = dopera
            self.allDesc.update(deepcopy(self.opera))




    def loadOperaDesc(self, dOperaAll,flog):

        if not self.name in dOperaAll.keys():
            print self.name, "Not in Opera table"
            flog.write(self.name + "\n")
            return

        self.Opera = dOperaAll[self.name]
        if not "allDesc" in self.__dict__:
            self.allDesc = self.Opera
        else:
            self.allDesc.update(deepcopy(dOperaAll[self.name]))


    def computeFP(self, typeFP):

        from rdkit.Chem.Fingerprints import FingerprintMols
        from rdkit.Chem import MACCSkeys
        from rdkit.Chem.AtomPairs import Pairs, Torsions
        from rdkit.Chem import AllChem

        if not "smiclean" in self.__dict__:
            self.log = self.log + "No smiles prepared\n"
            return 1
        else:
            self.mol = Chem.MolFromSmiles(self.smiclean)
            #print self.smiclean

        dFP = {}
        if typeFP == "Mol" or typeFP == "All":
            dFP["Mol"] = FingerprintMols.FingerprintMol(self.mol)
        if typeFP == "MACCS" or typeFP == "All":
            dFP["MACCS"] = MACCSkeys.GenMACCSKeys(self.mol)
        if typeFP == "pairs" or typeFP == "All":
            dFP["pairs"] = Pairs.GetAtomPairFingerprint(self.mol)
        if typeFP == "Torsion" or typeFP == "All":
            dFP["Torsion"] = Torsions.GetTopologicalTorsionFingerprint(self.mol)
        if typeFP == "Morgan" or typeFP == "All":
            dFP["Morgan"] = AllChem.GetMorganFingerprint(self.mol, 2)

        self.FP = dFP
        return 0


    def writeDesc(self, ldesc, filin):


        if "allDesc" in self.__dict__:
            lw = []
            for desc in ldesc:
                try: lw.append(str(self.allDesc[desc]))
                except: lw.append("NA")
            filin.write(self.name + "\t")
            filin.write("\t".join(lw) + "\n")

        else:
            self.log = self.log + "No descriptors computed to write\n"


    def writelog (self, prout):

        plog = prout + self.name + ".log"
        flog = open(plog, "w")
        flog.write(self.log)
        flog.close()



    def writeTablesDescCAS(self, prDescbyCAS):

        if "allDesc" in self.__dict__ and self.allDesc != {}:

            ptable = prDescbyCAS + self.name + ".txt"
            ftable = open(ptable, "w")
            ftable.write("CAS\t" + "\t".join(self.allDesc.keys()) + "\n")
            ftable.write(self.name)
            for desc in self.allDesc.keys():
                ftable.write("\t" + str(self.allDesc[desc]))
            ftable.write("\n")
            ftable.close()
            self.pdesc = ptable
            return 0
        else:
            self.log = self.log + "No descriptors computed for table\n"
            return 1


    def writeTablesDesc(self, prDescbyCAS, update = 0):

        if "allDesc" in self.__dict__ and self.allDesc != {}:

            ptable = prDescbyCAS + self.name + ".txt"
            if path.exists(ptable) and update == 0:
                return 0
            ftable = open(ptable, "w")
            ftable.write("ID\t" + "\t".join(self.allDesc.keys()) + "\n")
            ftable.write(self.name)
            for desc in self.allDesc.keys():
                ftable.write("\t" + str(self.allDesc[desc]))
            ftable.write("\n")
            ftable.close()
            self.pdesc = ptable
            return 0
        else:
            self.log = self.log + "Error: No descriptor computed for table\n"
            return 1