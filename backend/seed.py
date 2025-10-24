from server import app
from extensions import db
from models import Status, Artist, Tag, Track, Link

def seed_database():
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()
        
        # Statuses
        print('Seeding statuses...')
        idea = Status(name='Idea')
        demo = Status(name='Demo')
        in_progress = Status(name='In Progress')
        completed = Status(name='Completed')
        released = Status(name='Released')
        db.session.add_all([idea, demo, in_progress, completed, released])
        db.session.commit()

        # Artists
        print('Seeding artists...')
        beautifuls_dream = Artist(name='Beautifuls Dream')
        db.session.add_all([beautifuls_dream])
        db.session.commit()

        # Tags
        print('Seeding tags...')
        hip_hop = Tag(name='Hip-Hop')
        edm = Tag(name='EDM')
        country = Tag(name='Country')
        pop_punk = Tag(name='Pop-Punk')
        trap = Tag(name='Trap')
        drill = Tag(name='Drill')
        ai = Tag(name='AI')
        pop = Tag(name='Pop')
        emo = Tag(name='Emo')
        alternative = Tag(name='Alternative')
        chiptune = Tag(name='Chiptune')
        k_pop = Tag(name='K-Pop')
        sitcom = Tag(name='Sitcom')
        festival = Tag(name='Festival')
        prog_house = Tag(name='Prog-House')
        synth_pop = Tag(name='Synth-Pop')
        80s = Tag(name='80s')
        db.session.add_all([hip_hop, edm, country, pop_punk, trap, drill, ai, pop, emo, alternative, chiptune, k_pop, sitcom, festival, prog_house, synth_pop, 80s])
        db.session.commit()

        # Tracks
        print('Seeding tracks...')
        lettuce_guess = Track(
            title='lettuce-guess',
            artist_id=beautifuls_dream.id,
            status_id=released.id
        )
        teeth_meet_brush = Track(
            title='teeth-meet-brush',
            artist_id=beautifuls_dream.id,
            status_id=completed.id
        )
        all_the_chefs = Track(
            title='all-the-chefs',
            artist_id=beautifuls_dream.id,
            status_id=completed.id
        )
        cupcake_trampoline_the_other_one = Track(
            title='cupcake-trampoline-the-other-one',
            artist_id=beautifuls_dream.id,
            status_id=demo.id
        )
        apple_parade = Track(
            title='apple-parade',
            artist_id=beautifuls_dream.id,
            status_id=completed.id
        )
        army_crocs = Track(
            title='army-crocs',
            artist_id=beautifuls_dream.id,
            status_id=released.id
        )
        baby_pancake = Track(
            title='baby-pancake',
            artist_id=beautifuls_dream.id,
            status_id=released.id
        )
        db.session.add_all([lettuce_guess, teeth_meet_brush, all_the_chefs, cupcake_trampoline_the_other_one, apple_parade, army_crocs, baby_pancake])
        db.session.commit()

        # Track-Tag Relationships
        print('Adding tags to tracks...')
        lettuce_guess.tags.append(hip_hop)
        lettuce_guess.tags.append(trap)
        lettuce_guess.tags.append(drill)
        lettuce_guess.tags.append(ai)
        lettuce_guess.tags.append(emo)
        teeth_meet_brush.tags.append(hip_hop)
        teeth_meet_brush.tags.append(ai)
        teeth_meet_brush.tags.append(pop)
        teeth_meet_brush.tags.append(alternative)
        all_the_chefs.tags.append(ai)
        all_the_chefs.tags.append(chiptune)
        all_the_chefs.tags.append(k_pop)
        cupcake_trampoline_the_other_one.tags.append(pop_punk)
        cupcake_trampoline_the_other_one.tags.append(ai)
        apple_parade.tags.append(ai)
        apple_parade.tags.append(pop)
        army_crocs.tags.append(country)
        army_crocs.tags.append(ai)
        army_crocs.tags.append(pop)
        army_crocs.tags.append(festival)
        baby_pancake.tags.append(edm)
        baby_pancake.tags.append(ai)
        baby_pancake.tags.append(sitcom)
        baby_pancake.tags.append(festival)
        baby_pancake.tags.append(synth_pop)
        baby_pancake.tags.append(80s)
        db.session.commit()

        # Links
        print('Seeding links...')
        link_1 = Link(
            track_id=lettuce_guess.id,
            link_type='Songtrust',
            link_url='https://app.songtrust.com/songs/9456318'
        )
        link_2 = Link(
            track_id=lettuce_guess.id,
            link_type='Spotify',
            link_url='https://open.spotify.com/track/059dCf6zMaN5qSdmgRfzBM?si=5a681fd00ae64cab'
        )
        link_3 = Link(
            track_id=lettuce_guess.id,
            link_type='YouTube',
            link_url='https://www.youtube.com/watch?v=4JTjiuDU-6g'
        )
        link_4 = Link(
            track_id=teeth_meet_brush.id,
            link_type='YouTube',
            link_url='https://www.youtube.com/watch?v=WYSr56224J0&feature=youtu.be'
        )
        link_5 = Link(
            track_id=teeth_meet_brush.id,
            link_type='Songtrust',
            link_url='https://app.songtrust.com/songs/9457915'
        )
        link_6 = Link(
            track_id=teeth_meet_brush.id,
            link_type='DistroKid',
            link_url='https://distrokid.com/dashboard/album/?albumuuid=48727D2F-5883-44E2-802C882BDE20FE93'
        )
        link_7 = Link(
            track_id=lettuce_guess.id,
            link_type='DistroKid',
            link_url='https://distrokid.com/dashboard/album/?albumuuid=0DC3673C-9BEC-45B9-8E6CC17C730CCA1D'
        )
        link_8 = Link(
            track_id=lettuce_guess.id,
            link_type='assets_images',
            link_url='https://drive.google.com/drive/folders/1c1FjecoqJENRe6rA6buz762SytBTLCWr'
        )
        link_9 = Link(
            track_id=lettuce_guess.id,
            link_type='assets_videos',
            link_url='https://drive.google.com/drive/folders/1usP8DQpyY1Oc7mHgVn3lgGtk-ZlSmVEY?usp=drive_link'
        )
        link_10 = Link(
            track_id=lettuce_guess.id,
            link_type='assets_archive',
            link_url='https://drive.google.com/drive/folders/133mYbHbFK-51VOlzQkl9OtJw0NGb235f?usp=drive_link'
        )
        link_11 = Link(
            track_id=lettuce_guess.id,
            link_type='Images',
            link_url='https://drive.google.com/drive/folders/1u869ne0ylvocYEykoIuDON1AjRFdNNqH?usp=drive_link'
        )
        link_12 = Link(
            track_id=lettuce_guess.id,
            link_type='Audio',
            link_url='https://drive.google.com/drive/folders/1HpJ8ynAEHygYU6hxDDktLWxmdoMVOLKR'
        )
        link_13 = Link(
            track_id=lettuce_guess.id,
            link_type='Video',
            link_url='https://drive.google.com/file/d/1UlRln9iXLM0k582G4gQJFRlsNJ5Bsqs0/view?usp=drive_link'
        )
        link_14 = Link(
            track_id=lettuce_guess.id,
            link_type='Text',
            link_url='https://docs.google.com/document/d/1zi1k61ySbyQUQpp0dyQJwgVmP9xt-RKD2_jcECuACWs/edit?usp=drive_link'
        )
        link_15 = Link(
            track_id=teeth_meet_brush.id,
            link_type='Text',
            link_url='https://docs.google.com/document/d/1nwQORz8gR3oLfM0z3WyAuWCvTBscy5Q-fUkpCZpAQfo/edit?usp=drive_link'
        )
        link_16 = Link(
            track_id=teeth_meet_brush.id,
            link_type='assets_images',
            link_url='https://drive.google.com/drive/folders/1LoRoDycsKtXyth756s_po8Xo_qxebc9b'
        )
        link_17 = Link(
            track_id=teeth_meet_brush.id,
            link_type='assets_videos',
            link_url='https://drive.google.com/drive/folders/1qd_OBCgWGiQrNKXlNbEdtIHjp2WEaH6c?usp=drive_link'
        )
        link_18 = Link(
            track_id=teeth_meet_brush.id,
            link_type='Audio',
            link_url='https://drive.google.com/drive/folders/13eKkLYkj5w5zuuIDu76JPlvvpAwzYtB5?usp=drive_link'
        )
        link_19 = Link(
            track_id=teeth_meet_brush.id,
            link_type='assets_archive',
            link_url='https://drive.google.com/drive/folders/1aoTRTFYMocvZUkU0D-YKE0rdXXsoUiev?usp=drive_link'
        )
        link_20 = Link(
            track_id=teeth_meet_brush.id,
            link_type='Images',
            link_url='https://drive.google.com/drive/folders/15hCSnjWbyXz6ud7yXjDHkJCfV7qrFfZq?usp=drive_link'
        )
        link_21 = Link(
            track_id=all_the_chefs.id,
            link_type='YouTube',
            link_url='https://youtube.com/shorts/i4b6thAich8'
        )
        link_22 = Link(
            track_id=all_the_chefs.id,
            link_type='Images',
            link_url='https://drive.google.com/drive/folders/1wWRoq_31WMrnqtGpn5lgmMuBIQV3cno7?usp=drive_link'
        )
        link_23 = Link(
            track_id=all_the_chefs.id,
            link_type='Audio',
            link_url='https://drive.google.com/drive/folders/1wWRoq_31WMrnqtGpn5lgmMuBIQV3cno7?usp=drive_link'
        )
        link_24 = Link(
            track_id=teeth_meet_brush.id,
            link_type='Video',
            link_url='https://drive.google.com/file/d/1spbD-MKwaXgQffBF31Loq6ZKOJP3S_UF/view?usp=drive_link'
        )
        link_25 = Link(
            track_id=all_the_chefs.id,
            link_type='Video',
            link_url='https://drive.google.com/file/d/13QUlgGrOVKG3RFtcBTH4CCsx9oGZXpPV/view?usp=drive_link'
        )
        link_26 = Link(
            track_id=cupcake_trampoline_the_other_one.id,
            link_type='Video',
            link_url='https://drive.google.com/file/d/1sscr69IohaxPKv_SPJG3nwZo-EgH8uU3/view?usp=drive_link'
        )
        link_27 = Link(
            track_id=cupcake_trampoline_the_other_one.id,
            link_type='Images',
            link_url='https://drive.google.com/file/d/1wikssFO_MNgVHxJBrvfeyMYEwoaMcE3-/view?usp=drive_link'
        )
        link_28 = Link(
            track_id=apple_parade.id,
            link_type='YouTube',
            link_url='https://youtube.com/shorts/5749lBFRl8Y'
        )
        link_29 = Link(
            track_id=army_crocs.id,
            link_type='YouTube',
            link_url='https://www.youtube.com/watch?v=XNBJH8CTg5c'
        )
        link_30 = Link(
            track_id=army_crocs.id,
            link_type='Spotify',
            link_url='https://open.spotify.com/track/3M4kytKwWhmVNuNuqTsLbF?si=edac13dd489140ae'
        )
        link_31 = Link(
            track_id=army_crocs.id,
            link_type='DistroKid',
            link_url='https://distrokid.com/dashboard/album/?albumuuid=10DC475A-1029-4A94-BF0966D5C141E576'
        )
        link_32 = Link(
            track_id=army_crocs.id,
            link_type='Songtrust',
            link_url='https://app.songtrust.com/songs/9436553'
        )
        link_33 = Link(
            track_id=army_crocs.id,
            link_type='assets_archive',
            link_url='https://drive.google.com/drive/folders/1ArxZeBElMQubHjp2fzwAr0vmynyP-lfn?usp=drive_link'
        )
        link_34 = Link(
            track_id=army_crocs.id,
            link_type='assets_images',
            link_url='https://drive.google.com/drive/folders/1ziUZR5D0xRgp4ML3rE6fsnJ_HCe25TpK?usp=drive_link'
        )
        link_35 = Link(
            track_id=army_crocs.id,
            link_type='assets_videos',
            link_url='https://drive.google.com/drive/folders/1t--BFxxXNBnznBMVUdgpK21B9KIx2uGQ?usp=drive_link'
        )
        link_36 = Link(
            track_id=army_crocs.id,
            link_type='Audio',
            link_url='https://drive.google.com/drive/folders/1HmGHO4tJmAIfSWkU6UNmPJ8D_rIJlEE8?usp=drive_link'
        )
        link_37 = Link(
            track_id=army_crocs.id,
            link_type='Images',
            link_url='https://drive.google.com/drive/folders/1SFbLkB4HmGile_mKH4kKiW4YKA5eFBpK?usp=drive_link'
        )
        link_38 = Link(
            track_id=army_crocs.id,
            link_type='Text',
            link_url='https://docs.google.com/document/d/1f8SOuX9FRcMm2s_4lHKHynleO7hqYqH7CxRKzRPTAps/edit?tab=t.0'
        )
        link_39 = Link(
            track_id=baby_pancake.id,
            link_type='Text',
            link_url='https://docs.google.com/document/d/1MEItbPIUmFhqhrJl0crNDUVKLSlEwyNEyh5yCsdRBUk/edit?tab=t.0'
        )
        link_40 = Link(
            track_id=baby_pancake.id,
            link_type='YouTube',
            link_url='https://www.youtube.com/watch?v=aHUwU8PYV8g'
        )
        link_41 = Link(
            track_id=baby_pancake.id,
            link_type='Spotify',
            link_url='https://open.spotify.com/track/5mpbPCpLxathOgBmEK2FFL?si=752f1255fa8e41e6'
        )
        link_42 = Link(
            track_id=baby_pancake.id,
            link_type='DistroKid',
            link_url='https://distrokid.com/dashboard/album/?albumuuid=3C2DB873-5186-43F0-947A96EA0F276B57'
        )
        link_43 = Link(
            track_id=baby_pancake.id,
            link_type='Songtrust',
            link_url='https://app.songtrust.com/songs/9419995'
        )
        link_44 = Link(
            track_id=baby_pancake.id,
            link_type='assets_archive',
            link_url='https://drive.google.com/drive/folders/1C0zhv3UF7vdH59qkamRplrech4DWh5ep?usp=drive_link'
        )
        link_45 = Link(
            track_id=baby_pancake.id,
            link_type='assets_images',
            link_url='https://drive.google.com/drive/folders/15WW0jySX156ursJPALpldqoGhkpO91UH?usp=drive_link'
        )
        link_46 = Link(
            track_id=baby_pancake.id,
            link_type='assets_videos',
            link_url='https://drive.google.com/drive/folders/1YnaacmhvQOXK_WpO02ytlCOVb9qMj0p-?usp=drive_link'
        )
        link_47 = Link(
            track_id=baby_pancake.id,
            link_type='Images',
            link_url='https://drive.google.com/drive/folders/1KLFkeZRLwuHmDNzwQPKO50tiYYYTUbDV?usp=drive_link'
        )
        link_48 = Link(
            track_id=baby_pancake.id,
            link_type='Audio',
            link_url='https://drive.google.com/drive/folders/1VBeRvMuwq-TXt4i7w-IZ3q7-3sy8zEu7?usp=drive_link'
        )
        link_49 = Link(
            track_id=baby_pancake.id,
            link_type='Video',
            link_url='https://drive.google.com/file/d/1GZsDN6LDotRG55uWmHjLLCBpeEnqL1Ff/view?usp=drive_link'
        )
        link_50 = Link(
            track_id=army_crocs.id,
            link_type='Video',
            link_url='https://drive.google.com/file/d/1d65RJVEv29mfMqM1NL-CXNAl1jPvE4q1/view?usp=drive_link'
        )
        db.session.add_all([link_1, link_2, link_3, link_4, link_5, link_6, link_7, link_8, link_9, link_10, link_11, link_12, link_13, link_14, link_15, link_16, link_17, link_18, link_19, link_20, link_21, link_22, link_23, link_24, link_25, link_26, link_27, link_28, link_29, link_30, link_31, link_32, link_33, link_34, link_35, link_36, link_37, link_38, link_39, link_40, link_41, link_42, link_43, link_44, link_45, link_46, link_47, link_48, link_49, link_50])
        db.session.commit()

        print('✅ Database seeded successfully!')

if __name__ == '__main__':
    seed_database()
