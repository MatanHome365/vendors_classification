bucket_name = 'vendors-auto-assignment'

labels_to_keep = {'floor', 'mold', 'water', 'appliance', 'smoke', 'plant', 'flooring', 'curtain', 'appliance', 'switch',
                  'aluminium', 'shelf', 'dishwasher', 'shower curtain', 'cabinet', 'electronics', 'cushion',
                  'light fixture', 'monitor', 'chair', 'water', 'electrical device', 'adapter', 'wall', 'display',
                  'plug', 'furniture', 'electrical outlet', 'plant', 'couch', 'screen', 'wood', 'potty', 'bathroom',
                  'toilet', 'grille', 'window', 'cooler', 'door', 'air conditioner', 'tub', 'bathtub', 'plywood',
                  'jacuzzi', 'hot tub', 'sink', 'plumbing', 'sink faucet', 'wiring', 'shower faucet', 'ceiling light',
                  'shower', 'pump', 'machine', 'tap', 'washing', 'double sink', 'lighting', 'letterbox', 'postbox',
                  'mailbox', 'private mailbox', 'key', 'ceiling fan', 'skylight', 'keyboard', 'oven', 'tv', 'mailbox',
                  'porthole', 'dryer', 'washer', 'radiator', 'grove', 'petal', 'conifer', 'bush', 'grass', 'pine',
                  'palm tree', 'tree trunk', 'fir', 'fence', 'gate', 'door', 'grille', 'closet'}

clean_features = ['clean', 'cleaning', 'wipe', 'dump', 'trash', 'cleaner', 'dust', 'cleanup', 'filthy', 'garbage',
                  'dirty', 'mop', 'mopped', 'dumpster', 'dirt', 'vacuum']
carpet_cleaner_features = ['carpet', 'carpets']
garage_features = ['garage']
painter_features = ['paint', 'painter', 'repaint']
water_heater_features = ['water heater', 'hot water']
locksmith_features = ['unlock', 'lock', 'locksmith', 'key']
electrician_features = ['electric', 'electrical', 'lighting', 'light', 'electricity', 'wire', 'bulb', 'power', 'switch',
                        'wiring', 'generator', 'plug', 'circuit', 'fuse', 'outlet', 'socket', 'electrician', 'fan',
                        'energy', 'battery']
roofer_features = ['roof', 'ceiling', 'roofer']
mold_remediation_features = ['mold']
garden_features = ['yard', 'landscaping', 'branch', 'landscape', 'prune', 'garden', 'grass', 'sprinkler', 'gardener',
                   'rock', 'weed', 'irrigation', 'plant', 'tree', 'irrigate', 'bush', 'flower', 'lawn']

# define variables
thresh = 0.7
appliance_name = 'Appliance Installer / Repair'
hvac_name = 'HVAC'
exterminator_name = 'Exterminator'
pool_name = 'Pool/Hot Tub'
plumber_name = 'Plumber'
plumber_water_heater_name = 'Plumber (Water heater)'
garage_name = 'Garage Door Installer / Repair'
mold_name = 'Mold Remediation'
locksmith_name = 'Locksmith'
painter_name = 'Painter'
electrician_name = 'Electrician'
carpet_name = 'Carpet Cleaner'
cleaner_name = 'Cleaner'
gardener_name = 'Gardener and Landscape Architect'
roofer_name = 'Roofer'
contractor_name = 'General Contractor'
contractor_thresh = 2
index_categories = {0: mold_name, 1: locksmith_name, 2: carpet_name, 3: electrician_name, 4: painter_name, 5: cleaner_name, 6: gardener_name, 7: roofer_name}
categories_index = {mold_name: 0, locksmith_name: 1, carpet_name: 2, electrician_name: 3, painter_name: 4, cleaner_name: 5, gardener_name: 6, roofer_name: 7}

model_plumber_s3_address = 'models/svc_plumber_21_07.sav'
vect_plumber_s3_address = 'models/plumber_vect_21_07.pickel'
model_hvac_s3_address = 'models/svc_hvac_21_07.sav'
vect_hvac_s3_address = 'models/hvac_vect_21_07.pickel'
model_exterminator_s3_address = 'models/svc_exterminator_21_07.sav'
vect_exterminator_s3_address = 'models/exterminator_vect_21_07.pickel'
model_appliance_s3_address = 'models/svc_appliance_installer_21_07.sav'
vect_appliance_s3_address = 'models/appliance_installer_vect_21_07.pickel'
model_pool_s3_address = 'models/svc_pool_21_07.sav'
vect_pool_s3_address = 'models/pool_vect_21_07.pickel'

