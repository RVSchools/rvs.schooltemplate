import os

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

NAVIGATION_TABS = ['our-school', 
                   'principal',
                   'students',
                   'parents',
                   'staff',
                   'school-council',
                   'publications',
                   'contact-us',
                   'calendar',
                  ]

MEMBERS_ONLY_TABS = ['staff-room',
                     'plone-support-folder',
                    ]

WELCOME_TEXT = """<p>Welcome to your new school website.  Website guidelines, helpful information and site development support contact information can be found in Portal How To's.</p>
<p>Grade level collections will be created for you and will be displayed in the left hand portlet.</p>"""

SET_DEFAULT_PAGES = [('our-school', 'our-school'),
                     ('our-school/school-fee', 'school-fees'),
                     ('our-school/registration', 'how-to-register'),
                     ('principal', 'principals-message'),
                     ('students', 'student-information'),
                     ('parents', 'parent-information'),
                     ('staff', 'teacher-pages'),
                     ('school-council', 'meeting-dates'),
                     ('publications', 'publications-main'),
                     ('contact-us', 'contact-us'),
                     ('calendar', 'google-calendar'),
                     ('students/web-safety', 'web-safety'),
                    ]

LINKS = [
        ('our-school/emergency-response',
         'Emergency Response',
         'http://www.rockyview.ab.ca/parents/assets_parents/RVS-Parent-Summary.pdf'),
        ('our-school/registration/rvs-school-boundaries',
         'Attendance Areas',
         'http://www.rockyview.ab.ca/registration/attendanceareas'),
        ('our-school/registration/rvs-registration',
         'Register with Rocky View Schools!',
         'http://www.rockyview.ab.ca/registration'),
        ('our-school/rvs-transportation',
         'RVS Transportation',
         'http://www.rockyview.ab.ca/transportation'),
        ('our-school/school-forms',
         'School Forms',
         'http://www.rockyview.ab.ca'),
        ('our-school/school-calendar/rvs-school-calendar',
         'RVS School Calendar',
         'http://www.rockyview.ab.ca/jurisdiction/calendar'),
        ('our-school/school-fee/rvs-school-fees',
         'General School Fees',
         'http://www.rockyview.ab.ca/registration/schoolfees'),
        ('students/bell-times',
         'Bell Times',
         'http://www.rockyview.ab.ca'),
        ('students/rocky-view-sports',
         'Rocky View Sports',
         'http://rvsa.rockyview.ab.ca'),
        ('students/school-supplies',
         'School Supplies',
         'http://www.rockyview.ab.ca'),
        ('students/student-handbook',
         'Student Handbook',
         'http://www.rockyview.ab.ca'),
        ('students/student-links/student-links-on-rvs',
         'Digital Collection for Students',
         'http://www.rockyview.ab.ca/students'),
        ('parents/rvs-emergency-response',
         'Emergency Response',
         'http://www.rockyview.ab.ca/parents/assets_parents/RVS-Parent-Summary.pdf'),
        ('parents/student-handbook',
         'Student Handbook',
         'http://www.rockyview.ab.ca'),
        ('parents/inclement-weather',
         'Inclement Weather',
         'http://www.rockyview.ab.ca/transportation/inclementweather'),
        ('parents/teacher-pages',
         'Teacher Pages',
         'http://www.rockyview.ab.ca'),
        ('parents/parent-links/my-childs-learning',
         "My Child's Learning",
         'http://www.learnalberta.ca/content/mychildslearning/'),
        ('parents/parent-links/e-parenting',
         'E-Parenting',
         'http://www.parentfurther.com/e-parenting'),
        ('parents/parent-links/parent-links-rvs',
         'Parent News',
         'http://www.rockyview.ab.ca/parents'),
        ('parents/parent-links/the-role-of-the-parent',
         'Parents Role',
         'http://education.alberta.ca/parents/role.aspx'),
        ('staff/rvs-staff',
         'RVS Staff Information',
         'http://www.rockyview.ab.ca/staff'),
        ('school-council/rvs-school-council',
         'RVS School Council Info',
         'http://www.rockyview.ab.ca/parents/schoolcouncilswebportal'),
        ('contact-us/rocky-view-schools',
         'Rocky View Schools',
         'http://www.rockyview.ab.ca'),
        ('contact-us/rvs-transportation',
         'RVS Transportation',
         'http://www.rockyview.ab.ca/transportation'),
        ('staff-room/teacher-links/alberta-education-home',
         'Alberta Education',
         'http://www.education.alberta.ca/teachers.aspx'),
        ('staff-room/teacher-links/alberta-source',
         'Alberta Source',
         'http://www.albertasource.ca/'),
        ('staff-room/teacher-links/sysaid-helpdesk-ticket-system',
         'Sysaid Helpdesk Ticket System',
         'http://sysaid.rockyview.ab.ca/Login.jsp'),
        ('publications/rvs-communications',
         'Community News',
         'http://www.rockyview.ab.ca/publications/news'),
        ('plone-support/plone-tech-support',
         'Plone Support **NEW',
         'http://www.rockyview.ab.ca/techsupports/plone-1'),
        ]


def set_ms_mimetype_icons(portal):
    mtr = portal.mimetypes_registry
    extensions = set(['docx', 'xlsx', 'pptx'])
    icon_path = 'doc.png'
    mimetypes = [mt for mt in mtr.mimetypes() if extensions.intersection(
                    set(mt.extensions))]
    for mt in mimetypes:
        mt.icon_path = icon_path


def connect_images(portal):
    cur_dir = os.path.dirname(__file__)
    img_dir = '/'.join([cur_dir, 'images'])
    assets_paths = ['/{0}/assets/home-page-viewlets'.format(portal.id),
                    '/{0}/assets/teacher-page-viewlets'.format(portal.id)]
    images = dict(
        [(name, '/'.join([img_dir, name])) for name in os.listdir(img_dir)]
    )
    for path in assets_paths:
        folder = portal.unrestrictedTraverse(path)
        for img in folder.objectValues():
            if getattr(img, 'portal_type', '') == 'Image':
                filename = img.id
                if filename in images:
                    img_path = images[filename]
                    with open(img_path, 'rb') as img_file:
                        data = img_file.read()
                        field = img.Schema().get('image', None)
                        if field is not None:
                            field.set(img, data, filename=filename)


def template_setup(context):
    if context.readDataFile('rvs-template.txt') is None:
        return
    portal = context.getSite()
    qi = getToolByName(portal, 'portal_quickinstaller')
    if not qi.isProductInstalled('Products.CSSManager'):
        qi.installProduct('CSSManager')
    if not qi.isProductInstalled('Products.Marshall'):
        qi.installProduct('Marshall')
    wft = getToolByName(portal, 'portal_workflow')
    if 'newslisting' not in portal.objectIds():
        portal.invokeFactory('News Item', 'newslisting', title='Externally Published Site News Items Will Be Listed Here')
        newslisting = portal['newslisting']
        newslisting.reindexObject()
        wft.doActionFor(portal.newslisting, action='show_internally')
        wft.doActionFor(portal.newslisting, action='publish_internally')
        wft.doActionFor(portal.newslisting, action='publish_externally')
    if 'welcome' not in portal.objectIds():
        portal.invokeFactory('Topic', 'welcome', title='Welcome to RVS School', text=WELCOME_TEXT)
        portal.setDefaultPage('welcome')
        topic = portal['welcome']
        topic.reindexObject()
        type_criterion = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_criterion.setValue(['News Item'])
        state_criterion = topic.addCriterion('review_state', 'ATSimpleStringCriterion')
        state_criterion.setValue('externally_published')
        wft.doActionFor(portal.welcome, action='public')
        for folder_id in NAVIGATION_TABS:
            folder = getattr(portal, folder_id, None)
            if folder is not None:
                wft.doActionFor(folder, action='public')
        for folder_id in MEMBERS_ONLY_TABS:
            folder = getattr(portal, folder_id, None)
            if folder is not None:
                wft.doActionFor(folder, action='members')
        for folder, page in SET_DEFAULT_PAGES:
            folder_obj = portal.restrictedTraverse(folder)
            folder_obj.setDefaultPage(page)
        for link, title, url in LINKS:
            link_obj = portal.restrictedTraverse(link)
            link_obj.setTitle(title)
            link_obj.setRemoteUrl(url)

    # set the icon for xml-style ms mimetypes as doc.png (see issue #102)
    set_ms_mimetype_icons(portal)

    # attach image data to images created by structure import
    connect_images(portal)

    pc = getToolByName(portal, 'portal_catalog')
    for content in pc():
        try:
            content.getObject().allowDiscussion(False)
        except AttributeError:
            pass
    pc.refreshCatalog(clear=1)
