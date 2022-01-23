class Investment():
    def __init__(self, company_name, country, total_env_cost, work_capacity=0, fish_prod_capacity=0, crop_prod_capacity=0, meat_prod_capacity=0,
                 biodiversity=0, abio_rescs=0, water_prod_capacity=0, wood_prod_capacity=0):
        self.company_name = company_name
        self.country = country
        self.total_env_cost = int(total_env_cost)
        self.work_capacity = int(work_capacity)
        self.fish_prod_capacity = int(fish_prod_capacity)
        self.crop_prod_capacity = int(crop_prod_capacity)
        self.meat_prod_capacity = int(meat_prod_capacity)
        self.biodiversity = int(biodiversity)
        self.abio_rescs = int(abio_rescs)
        self.water_prod_capacity = int(water_prod_capacity)
        self.wood_prod_capacity = int(wood_prod_capacity)

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {} {} {}".format(self.company_name, self.country, self.total_env_cost, self.work_capacity, self.fish_prod_capacity, 
        self.crop_prod_capacity, self.meat_prod_capacity, self.biodiversity, self.abio_rescs, self.water_prod_capacity, self.wood_prod_capacity)