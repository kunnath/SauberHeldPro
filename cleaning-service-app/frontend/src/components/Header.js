import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaBars, FaTimes, FaPhone, FaEnvelope, FaUser, FaSignOutAlt } from 'react-icons/fa';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

const HeaderContainer = styled.header`
  background: ${props => props.theme.colors.white};
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
`;

const TopBar = styled.div`
  background: ${props => props.theme.colors.primary};
  color: white;
  padding: ${props => props.theme.spacing.xs} 0;
  font-size: 0.9rem;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: none;
  }
`;

const TopBarContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ContactInfo = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  
  span {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
`;

const LanguageSwitcher = styled.div`
  display: flex;
  gap: 0.5rem;
  align-items: center;
`;

const LanguageButton = styled.button`
  background: ${props => props.active ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: ${props => props.active ? 'bold' : 'normal'};
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.5);
  }
`;

const MainHeader = styled.div`
  padding: ${props => props.theme.spacing.sm} 0;
`;

const HeaderContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled(Link)`
  font-size: 1.8rem;
  font-weight: bold;
  color: ${props => props.theme.colors.primary};
  font-family: ${props => props.theme.fonts.heading};
  
  span {
    color: ${props => props.theme.colors.secondary};
  }
`;

const Nav = styled.nav`
  display: flex;
  gap: ${props => props.theme.spacing.lg};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: none;
  }
`;

const NavLink = styled(Link)`
  color: ${props => props.theme.colors.dark};
  font-weight: 500;
  transition: color 0.3s ease;
  position: relative;
  
  &:hover {
    color: ${props => props.theme.colors.primary};
  }
  
  &::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: ${props => props.theme.colors.primary};
    transition: width 0.3s ease;
  }
  
  &:hover::after {
    width: 100%;
  }
`;

const BookButton = styled(motion.button)`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.md};
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: none;
  }
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  color: ${props => props.theme.colors.primary};
  font-size: 1.5rem;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: block;
  }
`;

const MobileMenu = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: ${props => props.theme.colors.white};
  z-index: 2000;
  display: flex;
  flex-direction: column;
  padding: ${props => props.theme.spacing.lg};
`;

const MobileMenuHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const MobileNav = styled.nav`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.lg};
`;

const MobileNavLink = styled(Link)`
  color: ${props => props.theme.colors.dark};
  font-size: 1.2rem;
  font-weight: 500;
  padding: ${props => props.theme.spacing.sm} 0;
  border-bottom: 1px solid ${props => props.theme.colors.lightGray};
`;

const UserMenu = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  position: relative;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: none;
  }
`;

const UserButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: ${props => props.theme.colors.light};
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: 25px;
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.dark};
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    background: ${props => props.theme.colors.primary};
    color: white;
    border-color: ${props => props.theme.colors.primary};
  }
`;

const LogoutButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid ${props => props.theme.colors.danger};
  border-radius: 25px;
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.danger};
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    background: ${props => props.theme.colors.danger};
    color: white;
  }
`;

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const { currentLanguage, toggleLanguage, t } = useLanguage();
  const navigate = useNavigate();

  const handleBookNow = () => {
    navigate('/booking');
  };

  const handleLogout = () => {
    logout();
    navigate('/');
    setMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  return (
    <HeaderContainer>
      <TopBar>
        <div className="container">
          <TopBarContent>
            <ContactInfo>
              <span>
                <FaPhone /> +49 1577 2526898
              </span>
              <span>
                <FaEnvelope /> info@cleaningservice.de
              </span>
            </ContactInfo>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span>{t('english-german-support')}</span>
              <LanguageSwitcher>
                <LanguageButton 
                  active={currentLanguage === 'en'}
                  onClick={toggleLanguage}
                >
                  EN
                </LanguageButton>
                <LanguageButton 
                  active={currentLanguage === 'de'}
                  onClick={toggleLanguage}
                >
                  DE
                </LanguageButton>
              </LanguageSwitcher>
            </div>
          </TopBarContent>
        </div>
      </TopBar>
      
      <MainHeader>
        <div className="container">
          <HeaderContent>
            <Logo to="/">
              SauberHeld<span>Pro</span>
            </Logo>
            
            <Nav>
              <NavLink to="/">{t('home')}</NavLink>
              <NavLink to="/services">{t('services')}</NavLink>
              <NavLink to="/booking">{t('book-now')}</NavLink>
              <NavLink to="/contact">{t('contact')}</NavLink>
              {!isAuthenticated && <NavLink to="/login">{t('login')}</NavLink>}
            </Nav>
            
            {isAuthenticated ? (
              <UserMenu>
                <UserButton onClick={() => navigate('/dashboard')}>
                  <FaUser />
                  {user?.first_name || t('dashboard')}
                </UserButton>
                <LogoutButton onClick={handleLogout}>
                  <FaSignOutAlt />
                  {t('logout')}
                </LogoutButton>
              </UserMenu>
            ) : (
              <BookButton
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/login')}
              >
                {t('login')}
              </BookButton>
            )}
            
            <MobileMenuButton onClick={toggleMobileMenu}>
              <FaBars />
            </MobileMenuButton>
          </HeaderContent>
        </div>
      </MainHeader>
      
      {mobileMenuOpen && (
        <MobileMenu
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          transition={{ type: 'tween', duration: 0.3 }}
        >
          <MobileMenuHeader>
            <Logo to="/" onClick={closeMobileMenu}>
              Clean<span>Pro</span>
            </Logo>
            <button onClick={toggleMobileMenu}>
              <FaTimes />
            </button>
          </MobileMenuHeader>
          
          <MobileNav>
            <MobileNavLink to="/" onClick={closeMobileMenu}>{t('home')}</MobileNavLink>
            <MobileNavLink to="/services" onClick={closeMobileMenu}>{t('services')}</MobileNavLink>
            <MobileNavLink to="/booking" onClick={closeMobileMenu}>{t('book-now')}</MobileNavLink>
            <MobileNavLink to="/contact" onClick={closeMobileMenu}>{t('contact')}</MobileNavLink>
            {isAuthenticated ? (
              <>
                <MobileNavLink to="/dashboard" onClick={closeMobileMenu}>{t('dashboard')}</MobileNavLink>
                <MobileNavLink to="#" onClick={handleLogout}>{t('logout')}</MobileNavLink>
              </>
            ) : (
              <MobileNavLink to="/login" onClick={closeMobileMenu}>{t('login')}</MobileNavLink>
            )}
          </MobileNav>
        </MobileMenu>
      )}
    </HeaderContainer>
  );
};

export default Header;
