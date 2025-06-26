import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaCheck, FaBolt, FaShieldAlt, FaClock, FaHome, FaBuilding, FaGem } from 'react-icons/fa';
import { useLanguage } from '../contexts/LanguageContext';

const ServicesContainer = styled.div`
  padding: ${props => props.theme.spacing.xl} 0;
`;

const HeroSection = styled.section`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.xxl} 0;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: 2rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.3rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
`;

const ServicesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: ${props => props.theme.spacing.xl};
  margin: ${props => props.theme.spacing.xxl} 0;
`;

const ServiceCard = styled(motion.div)`
  background: white;
  border-radius: 15px;
  padding: ${props => props.theme.spacing.xl};
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: ${props => props.theme.colors.secondary};
    transform: translateY(-5px);
  }
`;

const ServiceIcon = styled.div`
  font-size: 3rem;
  color: ${props => props.theme.colors.secondary};
  margin-bottom: ${props => props.theme.spacing.md};
`;

const ServiceTitle = styled.h3`
  font-size: 1.8rem;
  color: ${props => props.theme.colors.dark};
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const ServicePrice = styled.div`
  color: ${props => props.theme.colors.secondary};
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: ${props => props.theme.spacing.md};
`;

const ServiceDescription = styled.p`
  color: ${props => props.theme.colors.gray};
  margin-bottom: ${props => props.theme.spacing.lg};
  line-height: 1.6;
`;

const FeaturesList = styled.ul`
  list-style: none;
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const FeatureItem = styled.li`
  display: flex;
  align-items: center;
  margin-bottom: ${props => props.theme.spacing.xs};
  color: ${props => props.theme.colors.gray};
  
  svg {
    color: ${props => props.theme.colors.success};
    margin-right: ${props => props.theme.spacing.xs};
  }
`;

const BookButton = styled(motion.button)`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.xl};
  border: none;
  border-radius: 8px;
  font-weight: 600;
  width: 100%;
  font-size: 1.1rem;
`;

const ComparisonSection = styled.section`
  background: ${props => props.theme.colors.light};
  padding: ${props => props.theme.spacing.xxl} 0;
  margin: ${props => props.theme.spacing.xxl} 0;
`;

const ComparisonTable = styled.div`
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 1000px;
  margin: 0 auto;
`;

const TableHeader = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  background: ${props => props.theme.colors.secondary};
  color: white;
  font-weight: 600;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
    text-align: center;
  }
`;

const TableRow = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  border-bottom: 1px solid ${props => props.theme.colors.lightGray};
  
  &:last-child {
    border-bottom: none;
  }
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
    text-align: center;
  }
`;

const TableCell = styled.div`
  padding: ${props => props.theme.spacing.md};
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:first-child {
    justify-content: flex-start;
    font-weight: 600;
  }
`;

const SectionTitle = styled.h2`
  text-align: center;
  font-size: 2.5rem;
  color: ${props => props.theme.colors.dark};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const ServicesPage = () => {
  const { t } = useLanguage();

  // Define service features in the component since they're arrays
  const basicFeatures = [
    t('basic-feature-1'),
    t('basic-feature-2'), 
    t('basic-feature-3'),
    t('basic-feature-4'),
    t('basic-feature-5')
  ];

  const deepFeatures = [
    t('deep-feature-1'),
    t('deep-feature-2'),
    t('deep-feature-3'), 
    t('deep-feature-4'),
    t('deep-feature-5')
  ];

  const officeFeatures = [
    t('office-feature-1'),
    t('office-feature-2'),
    t('office-feature-3'),
    t('office-feature-4'), 
    t('office-feature-5')
  ];

  const services = [
    {
      icon: <FaHome />,
      title: t('basic-cleaning'),
      price: t('basic-cleaning-price'),
      description: t('basic-cleaning-detailed'),
      features: basicFeatures,
      duration: t('basic-duration'),
      ideal: t('basic-ideal')
    },
    {
      icon: <FaGem />,
      title: t('deep-cleaning'),
      price: t('deep-cleaning-price'),
      description: t('deep-cleaning-detailed'),
      features: deepFeatures,
      duration: t('deep-duration'),
      ideal: t('deep-ideal')
    },
    {
      icon: <FaBuilding />,
      title: t('office-cleaning'),
      price: t('office-cleaning-price'),
      description: t('office-cleaning-detailed'),
      features: officeFeatures,
      duration: t('office-duration'),
      ideal: t('office-ideal')
    }
  ];

  const comparisonData = [
    { feature: t('dusting-surface-cleaning'), basic: true, deep: true, office: true },
    { feature: t('vacuuming'), basic: true, deep: true, office: true },
    { feature: t('kitchen-cleaning'), basic: true, deep: true, office: true },
    { feature: t('bathroom-sanitizing'), basic: true, deep: true, office: true },
    { feature: t('trash-removal'), basic: true, deep: true, office: true },
    { feature: t('inside-appliances'), basic: false, deep: true, office: false },
    { feature: t('baseboards-details'), basic: false, deep: true, office: false },
    { feature: t('window-cleaning-interior'), basic: false, deep: true, office: false },
    { feature: t('workspace-sanitizing'), basic: false, deep: false, office: true },
    { feature: t('conference-room-setup'), basic: false, deep: false, office: true }
  ];

  return (
    <ServicesContainer>
      <HeroSection>
        <div className="container">
          <Title>{t('our-cleaning-services')}</Title>
          <Subtitle>
            {t('professional-solutions-subtitle')}
          </Subtitle>
        </div>
      </HeroSection>

      <div className="container">
        <ServicesGrid>
          {services.map((service, index) => (
            <ServiceCard
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.02 }}
            >
              <ServiceIcon>{service.icon}</ServiceIcon>
              <ServiceTitle>{service.title}</ServiceTitle>
              <ServicePrice>{service.price}</ServicePrice>
              <ServiceDescription>{service.description}</ServiceDescription>
              
              <FeaturesList>
                {service.features.map((feature, idx) => (
                  <FeatureItem key={idx}>
                    <FaCheck />
                    {feature}
                  </FeatureItem>
                ))}
              </FeaturesList>
              
              <div style={{ marginBottom: '1rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px' }}>
                <strong>{t('duration')}:</strong> {service.duration}<br />
                <strong>{t('ideal-for')}:</strong> {service.ideal}
              </div>
              
              <BookButton
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => window.location.href = '/booking'}
              >
                {t('book-now')}
              </BookButton>
            </ServiceCard>
          ))}
        </ServicesGrid>
      </div>

      <ComparisonSection>
        <div className="container">
          <SectionTitle>{t('service-comparison')}</SectionTitle>
          <ComparisonTable>
            <TableHeader>
              <TableCell>{t('features')}</TableCell>
              <TableCell>{t('basic-cleaning')}</TableCell>
              <TableCell>{t('deep-cleaning')}</TableCell>
              <TableCell>{t('office-cleaning')}</TableCell>
            </TableHeader>
            
            {comparisonData.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.feature}</TableCell>
                <TableCell>
                  {row.basic ? (
                    <FaCheck style={{ color: '#28a745' }} />
                  ) : (
                    <span style={{ color: '#ccc' }}>−</span>
                  )}
                </TableCell>
                <TableCell>
                  {row.deep ? (
                    <FaCheck style={{ color: '#28a745' }} />
                  ) : (
                    <span style={{ color: '#ccc' }}>−</span>
                  )}
                </TableCell>
                <TableCell>
                  {row.office ? (
                    <FaCheck style={{ color: '#28a745' }} />
                  ) : (
                    <span style={{ color: '#ccc' }}>−</span>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </ComparisonTable>
        </div>
      </ComparisonSection>

      <div className="container">
        <SectionTitle>{t('why-choose-services')}</SectionTitle>
        <ServicesGrid style={{ marginTop: '2rem' }}>
          <ServiceCard
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <ServiceIcon><FaBolt /></ServiceIcon>
            <ServiceTitle>{t('quick-efficient')}</ServiceTitle>
            <ServiceDescription>
              {t('quick-efficient-desc')}
            </ServiceDescription>
          </ServiceCard>

          <ServiceCard
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <ServiceIcon><FaShieldAlt /></ServiceIcon>
            <ServiceTitle>{t('fully-insured')}</ServiceTitle>
            <ServiceDescription>
              {t('fully-insured-desc')}
            </ServiceDescription>
          </ServiceCard>

          <ServiceCard
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            viewport={{ once: true }}
          >
            <ServiceIcon><FaClock /></ServiceIcon>
            <ServiceTitle>{t('flexible-scheduling')}</ServiceTitle>
            <ServiceDescription>
              {t('flexible-scheduling-detailed')}
            </ServiceDescription>
          </ServiceCard>
        </ServicesGrid>
      </div>
    </ServicesContainer>
  );
};

export default ServicesPage;
