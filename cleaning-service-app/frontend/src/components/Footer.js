import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { FaPhone, FaEnvelope, FaMapMarkerAlt, FaClock, FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';

const FooterContainer = styled.footer`
  background: ${props => props.theme.colors.dark};
  color: ${props => props.theme.colors.white};
  padding: ${props => props.theme.spacing.xl} 0 ${props => props.theme.spacing.lg} 0;
  margin-top: ${props => props.theme.spacing.xl};
`;

const FooterContent = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${props => props.theme.spacing.xl};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const FooterSection = styled.div`
  h4 {
    color: ${props => props.theme.colors.secondary};
    margin-bottom: ${props => props.theme.spacing.md};
    font-size: 1.2rem;
  }
`;

const FooterList = styled.ul`
  list-style: none;
  
  li {
    margin-bottom: ${props => props.theme.spacing.xs};
  }
`;

const FooterLink = styled(Link)`
  color: #ccc;
  transition: color 0.3s ease;
  
  &:hover {
    color: ${props => props.theme.colors.white};
  }
`;

const ContactItem = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  margin-bottom: ${props => props.theme.spacing.xs};
  color: #ccc;
  
  svg {
    color: ${props => props.theme.colors.secondary};
  }
`;

const SocialLinks = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.sm};
  margin-top: ${props => props.theme.spacing.md};
  
  a {
    color: #ccc;
    font-size: 1.5rem;
    transition: color 0.3s ease;
    
    &:hover {
      color: ${props => props.theme.colors.secondary};
    }
  }
`;

const FooterBottom = styled.div`
  border-top: 1px solid #555;
  padding-top: ${props => props.theme.spacing.lg};
  text-align: center;
  color: #999;
  
  p {
    margin-bottom: ${props => props.theme.spacing.xs};
  }
`;

const PaymentMethods = styled.div`
  display: flex;
  justify-content: center;
  gap: ${props => props.theme.spacing.sm};
  margin-top: ${props => props.theme.spacing.md};
  
  img {
    height: 30px;
    opacity: 0.7;
    transition: opacity 0.3s ease;
    
    &:hover {
      opacity: 1;
    }
  }
`;

const Footer = () => {
  return (
    <FooterContainer>
      <div className="container">
        <FooterContent>
          <FooterSection>
            <h4>Quick Links</h4>
            <FooterList>
              <li><FooterLink to="/">Home</FooterLink></li>
              <li><FooterLink to="/services">Services</FooterLink></li>
              <li><FooterLink to="/booking">Book Now</FooterLink></li>
              <li><FooterLink to="/contact">Contact</FooterLink></li>
              <li><FooterLink to="/about">About</FooterLink></li>
              <li><FooterLink to="/faq">FAQ</FooterLink></li>
            </FooterList>
          </FooterSection>
          
          <FooterSection>
            <h4>Services</h4>
            <FooterList>
              <li><FooterLink to="/services/basic">Basic Cleaning</FooterLink></li>
              <li><FooterLink to="/services/deep">Deep Cleaning</FooterLink></li>
              <li><FooterLink to="/services/office">Office Cleaning</FooterLink></li>
              <li><FooterLink to="/services/regular">Regular Cleaning</FooterLink></li>
              <li><FooterLink to="/services/move">Move-In/Out Cleaning</FooterLink></li>
              <li><FooterLink to="/services/sanitization">Sanitization</FooterLink></li>
            </FooterList>
          </FooterSection>
          
          <FooterSection>
            <h4>Contact Info</h4>
            <ContactItem>
              <FaPhone />
              <span>+49 1577 2526898</span>
            </ContactItem>
            <ContactItem>
              <FaEnvelope />
              <span>info@cleaningservice.de</span>
            </ContactItem>
            <ContactItem>
              <FaMapMarkerAlt />
              <span>Hauptstr 117, 10827 Berlin, Deutschland</span>
            </ContactItem>
            <ContactItem>
              <FaClock />
              <span>8am - 6pm (Mon-Sun)</span>
            </ContactItem>
            
            <SocialLinks>
              <a href="#" aria-label="Facebook"><FaFacebook /></a>
              <a href="#" aria-label="Twitter"><FaTwitter /></a>
              <a href="#" aria-label="Instagram"><FaInstagram /></a>
              <a href="#" aria-label="LinkedIn"><FaLinkedin /></a>
            </SocialLinks>
          </FooterSection>
          
          <FooterSection>
            <h4>Legal</h4>
            <FooterList>
              <li><FooterLink to="/terms">Terms & Conditions</FooterLink></li>
              <li><FooterLink to="/privacy">Privacy Policy</FooterLink></li>
              <li><FooterLink to="/imprint">Imprint</FooterLink></li>
              <li><FooterLink to="/cookies">Cookie Policy</FooterLink></li>
            </FooterList>
            
            <h4 style={{ marginTop: '2rem' }}>Trusted Company</h4>
            <p style={{ color: '#999', fontSize: '0.9rem' }}>
              Professional Cleaning Services<br />
              Licensed & Insured<br />
              Est. 2016
            </p>
          </FooterSection>
        </FooterContent>
        
        <FooterBottom>
          <p>© 2025 GRK Dienstleistungen. All rights reserved.</p>
          <p>GRK Dienstleistungen | Hauptstr 117, 10827 Berlin, Deutschland | Registry Code: DE123456789</p>
          
          <PaymentMethods>
            <div style={{ 
              background: '#fff', 
              padding: '5px 10px', 
              borderRadius: '5px', 
              fontSize: '0.8rem', 
              color: '#333' 
            }}>
              VISA
            </div>
            <div style={{ 
              background: '#fff', 
              padding: '5px 10px', 
              borderRadius: '5px', 
              fontSize: '0.8rem', 
              color: '#333' 
            }}>
              MasterCard
            </div>
            <div style={{ 
              background: '#fff', 
              padding: '5px 10px', 
              borderRadius: '5px', 
              fontSize: '0.8rem', 
              color: '#333' 
            }}>
              PayPal
            </div>
            <div style={{ 
              background: '#fff', 
              padding: '5px 10px', 
              borderRadius: '5px', 
              fontSize: '0.8rem', 
              color: '#333' 
            }}>
              SEPA
            </div>
          </PaymentMethods>
        </FooterBottom>
      </div>
    </FooterContainer>
  );
};

export default Footer;
