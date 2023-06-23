import streamlit as st
from selenium import webdriver
from utilities import *
import json

def welcome():
    #Title, subheader and image for welcome page
    st.title('Job Buddy')
    st.subheader('Sadak se uthake star bana dega')
    
    st.subheader('Helps to ease your apply process')
    st.image("data:image/jpeg;base64,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",use_column_width=True)

def linkedin_improver():
    profile_url = st.text_input('Enter your linkedin profile link')
    driver = webdriver.Chrome(executable_path= r"/Users/sankalpjain/Downloads/chromedriver_mac64/chromedriver")
    login(driver)
    if profile_url:
        driver.get(profile_url) 
        time.sleep(3)
        src = driver.page_source
        
        # Now using beautiful soup
        soup = BeautifulSoup(src, 'lxml')

        #Extracting sections
        sections = {}
        sections['Basic Info'] = get_basic_info(driver,soup)
        sections['About'] = extract_section(driver,soup,'About')
        sections['Experience'] = extract_section(driver,soup,name = 'Experience')
        sections['Education'] = extract_section(driver,soup,'Education')
        sections['Licenses & certifications'] = extract_section(driver,soup,name = 'Licenses & certifications')
        sections['Volunteering'] = extract_section(driver,soup,'Volunteering')
        sections['Recommendations'] = extract_section(driver,soup,'Recommendations')
        sections['Honors & awards'] = extract_section(driver, soup,'Honors & awards')
        sections['Projects'] = extract_section(driver,soup,'Projects')
        sections['Skills'] = extract_section(driver,soup,'Skills')
        sections['Organizations'] = extract_section(driver,soup,'Organizations')
        # Closes the current window
        driver.close()

        if sections['Basic Info']['images']['dp']:
            st.image(sections['Basic Info']['images']['dp'])


        missing_sections = []
        for name, section in sections.items():
            if not section:
                missing_sections.append(name)
        
        if len(missing_sections)>0:
            st.title('Missing Sections :')
            for section in missing_sections:
                st.write('• '+section)
        for name, section in sections.items():
            if not section:
                continue
            st.title(name)
            if name=='About':
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader('Current')
                    st.write(section)
                
                with col2:
                    st.subheader('Improved')
                    new_about = improve_content(section)
                    st.write(new_about)
            elif name=='Basic Info':
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader('Current')
                    for n,v in sections['Basic Info'].items():
                        if n=='images':
                            continue
                        if n=='contact_info':
                            st.write(n+':')
                            for na, info in v.items():
                                st.text('    {} : {}'.format(na, info))
                        else:
                            st.write('{} : {}'.format(n,v))
                
                with col2:
                    st.subheader('Improved')
                    imp = basic_improvements(sections['Basic Info'])
                    for n,v in imp.items():
                        st.write("{} : {}".format(n,v))
                with open("info.json", "w") as outfile:
                    sections_copy = sections.copy()
                    del sections_copy['Basic Info']['images']
                    json.dump(sections_copy, outfile)

            else:
                for section_item in section:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader('Current')
                    for property in section_item.values():
                        with col1:
                            st.write(property)
                    with col2:
                        st.subheader('Improved')
                        if len(list(section_item.values())[-1])<150:
                            st.write(improve_content("generate my {} description for my linkedin profile in bullet points - ".format(name) + '. '.join(list(section_item.values()))))
                        else:
                            st.write(improve_content("improve my {} description for my linkedin profile in bullet points - ".format(name) + list(section_item.values())[-1]))


        

def main():
    #Three Options to select for user
    selected_box = st.sidebar.selectbox('Choose one of the following', ('Welcome', 'LinkedIn improver'))

    #Welcome page
    if selected_box == 'Welcome':
        welcome()

    #Hairtransfer page 
    if selected_box == 'LinkedIn improver':
        linkedin_improver()
    
if __name__ == "__main__":
    main()