from .SettingsSeeder import SettingsSeeder


def db_seed():
    seeders = {
        'SettingsSeeder': SettingsSeeder
    }
    for seeder_name, seeder in seeders.items():
        error = seeder.run()
        if error:
            print(f'While running {seeder_name} following error raised:')
            print(error)
            break
        print(f'Successfully run {seeder_name}!')
