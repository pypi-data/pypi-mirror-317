//
//  Cell.h
//  ttcr
//
//  Created by Bernard Giroux on 16-02-27.
//  Copyright © 2016 Bernard Giroux. All rights reserved.
//

/*
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef ttcr_Cell_h
#define ttcr_Cell_h

#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

#include "ttcr_t.h"

namespace ttcr {

    template <typename T, typename NODE, typename S>
    class Cell {
    public:
        Cell(const size_t n) : slowness(std::vector<T>(n)) { }

        void setSlowness(const std::vector<T>& s) {
            if ( slowness.size() != s.size() ) {
                throw std::length_error("Error: slowness vectors of incompatible size.");
            }
            slowness = s;
        }

        const T getSlowness(const size_t i) const {
            return slowness.at(i);
        }

        void setXi(const std::vector<T>& s) {
            throw std::logic_error("Error: xi not defined for Cell.");
        }

        void setChi(const std::vector<T>& s) {
            throw std::logic_error("Error: chi not defined for Cell.");
        }

        void setPsi(const std::vector<T>& s) {
            throw std::logic_error("Error: psi not defined for Cell.");
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for Cell.");
        }

        void setVp0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vp0 not defined for Cell.");
        }

        void setVs0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vs0 not defined for Cell.");
        }

        void setDelta(const std::vector<T>& s) {
            throw std::logic_error("Error: delta not defined for Cell.");
        }

        void setEpsilon(const std::vector<T>& s) {
            throw std::logic_error("Error: epsilon not defined for Cell.");
        }

        void setGamma(const std::vector<T>& s) {
            throw std::logic_error("Error: gamma not defined for Cell.");
        }
        
        void setS2(const std::vector<T>& r) {
            throw std::logic_error("Error: s2 not defined for Cell.");
        }
    
        void setS4(const std::vector<T>& r) {
            throw std::logic_error("Error: s4 not defined for Cell.");
        }

        T computeDt(const S& source, const S& node,
                    const size_t cellNo) const {
            return slowness[cellNo] * source.getDistance( node );
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            return slowness[cellNo] * source.getDistance( node );
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            return slowness[cellNo] * source.getDistance( node );
        }
        
        void computeDistance(const NODE& source, const S& node,
                             siv<T>& cell) const {
            cell.v = source.getDistance( node );
        }
        void computeDistance(const NODE& source, const S& node,
                             siv2<T>& cell) const {
            cell.v = source.getDistance( node );
        }

    private:
        std::vector<T> slowness;
    };


    // Elliptical anisotropy in 2D (Y Dimension ignored)

    template <typename T, typename NODE, typename S>
    class CellElliptical {
    public:
        CellElliptical(const size_t n) :
        slowness(std::vector<T>(n)),
        xi(std::vector<T>(n,0.0)) {
        }

        void setSlowness(const std::vector<T>& s) {
            if ( slowness.size() != s.size() ) {
                throw std::length_error("Error: slowness vectors of incompatible size.");
            }
            slowness = s;
        }

        const T getSlowness(const size_t i) const {
            return slowness.at(i);
        }

        void setXi(const std::vector<T>& s) {
            if ( xi.size() != s.size() ) {
                throw std::length_error("Error: xi vectors of incompatible size.");
            }
            for ( size_t n=0; n<xi.size(); ++n ) {
                xi[n] = s[n]*s[n];
            }
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for CellElliptical.");
        }

        void setVp0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vp0 not defined for CellElliptical.");
        }

        void setVs0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vs0 not defined for CellElliptical.");
        }

        void setDelta(const std::vector<T>& s) {
            throw std::logic_error("Error: delta not defined for CellElliptical.");
        }

        void setEpsilon(const std::vector<T>& s) {
            throw std::logic_error("Error: epsilon not defined for CellElliptical.");
        }

        void setGamma(const std::vector<T>& s) {
            throw std::logic_error("Error: gamma not defined for CellElliptical.");
        }

        void setS2(const std::vector<T>& r) {
            throw std::logic_error("Error: s2 not defined for CellElliptical.");
        }
    
        void setS4(const std::vector<T>& r) {
            throw std::logic_error("Error: s4 not defined for CellElliptical.");
        }

        T computeDt(const S& source, const S& node,
                    const size_t cellNo) const {
            T lx = node.x - source.x;
            T lz = node.z - source.z;
            return slowness[cellNo] * std::sqrt( lx*lx + xi[cellNo]*lz*lz );
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            T lx = node.x - source.getX();
            T lz = node.z - source.getZ();
            return slowness[cellNo] * std::sqrt( lx*lx + xi[cellNo]*lz*lz );
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            T lx = node.getX() - source.getX();
            T lz = node.getZ() - source.getZ();
            return slowness[cellNo] * std::sqrt( lx*lx + xi[cellNo]*lz*lz );
        }

        void computeDistance(const NODE& source, const S& node,
                             siv<T>& cell) const {
            assert(false);  // we should not end up here
            cell.v  = std::sqrt((node.x - source.getX())*(node.x - source.getX()) +
                                (node.z - source.getZ())*(node.z - source.getZ()));
        }
        void computeDistance(const NODE& source, const S& node,
                             siv2<T>& cell) const {
            cell.v  = std::abs(node.x - source.getX());
            cell.v2 = std::abs(node.z - source.getZ());
        }

    private:
        std::vector<T> slowness;
        std::vector<T> xi;        // anisotropy ratio, xi = sz / sx, *** squared ***
    };


    // Elliptical anisotropy in 2D (Y Dimension ignored)

    template <typename T, typename NODE, typename S>
    class CellTiltedElliptical {
    public:
        CellTiltedElliptical(const size_t n) :
        slowness(std::vector<T>(n)),
        xi(std::vector<T>(n,0.0)),
        tAngle(std::vector<T>(n,0.0)),
        ca(std::vector<T>(n,1.0)),
        sa(std::vector<T>(n,0.0)) {
        }

        void setSlowness(const std::vector<T>& s) {
            if ( slowness.size() != s.size() ) {
                throw std::length_error("Error: slowness vectors of incompatible size.");
            }
            slowness = s;
        }

        const T getSlowness(const size_t i) const {
            return slowness.at(i);
        }

        void setXi(const std::vector<T>& s) {
            if ( xi.size() != s.size() ) {
                throw std::length_error("Error: xi vectors of incompatible size.");
            }
            for ( size_t n=0; n<xi.size(); ++n ) {
                xi[n] = s[n]*s[n];
            }
        }

        void setTiltAngle(const std::vector<T>& s) {
            if ( tAngle.size() != s.size() ) {
                throw std::length_error("Error: angle vectors of incompatible size.");
            }
            for ( size_t n=0; n<tAngle.size(); ++n ) {
                tAngle[n] = s[n];
                ca[n] = std::cos(s[n]);
                sa[n] = std::sin(s[n]);
            }
        }

        void setVp0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vp0 not defined for CellTiltedElliptical.");
        }

        void setVs0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vs0 not defined for CellTiltedElliptical.");
        }

        void setDelta(const std::vector<T>& s) {
            throw std::logic_error("Error: delta not defined for CellTiltedElliptical.");
        }

        void setEpsilon(const std::vector<T>& s) {
            throw std::logic_error("Error: epsilon not defined for CellTiltedElliptical.");
        }

        void setGamma(const std::vector<T>& s) {
            throw std::logic_error("Error: gamma not defined for CellTiltedElliptical.");
        }

        void setS2(const std::vector<T>& r) {
            throw std::logic_error("Error: s2 not defined for CellTiltedElliptical.");
        }
    
        void setS4(const std::vector<T>& r) {
            throw std::logic_error("Error: s4 not defined for CellTiltedElliptical.");
        }

        T computeDt(const S& source, const S& node,
                    const size_t cellNo) const {
            T lx = node.x - source.x;
            T lz = node.z - source.z;
            T t1 = lx * ca[cellNo] + lz * sa[cellNo];
            T t2 = lz * ca[cellNo] - lx * sa[cellNo];

            return slowness[cellNo] * std::sqrt( t1*t1 + xi[cellNo]*t2*t2 );
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            T lx = node.x - source.getX();
            T lz = node.z - source.getZ();
            T t1 = lx * ca[cellNo] + lz * sa[cellNo];
            T t2 = lz * ca[cellNo] - lx * sa[cellNo];

            return slowness[cellNo] * std::sqrt( t1*t1 + xi[cellNo]*t2*t2 );
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            T lx = node.getX() - source.getX();
            T lz = node.getZ() - source.getZ();
            T t1 = lx * ca[cellNo] + lz * sa[cellNo];
            T t2 = lz * ca[cellNo] - lx * sa[cellNo];

            return slowness[cellNo] * std::sqrt( t1*t1 + xi[cellNo]*t2*t2 );
        }

        void computeDistance(const NODE& source, const S& node,
                             siv<T>& cell) const {
            assert(false);  // we should not end up here
            cell.v  = std::sqrt((node.x - source.getX())*(node.x - source.getX()) +
                                (node.z - source.getZ())*(node.z - source.getZ()));
        }
        void computeDistance(const NODE& source, const S& node,
                             siv2<T>& cell) const {
            cell.v  = std::abs(node.x - source.getX());
            cell.v2 = std::abs(node.z - source.getZ());
        }

    private:
        std::vector<T> slowness;
        std::vector<T> xi;        // anisotropy ratio, xi = sz / sx, *** squared ***
        std::vector<T> tAngle;    // column-wise (z axis) anisotropy angle of the cells, in radians
        std::vector<T> ca;        // cosine of tAngle
        std::vector<T> sa;        // sine of tAngle
    };


    //  VTI anisotropy, P or SV phase, in 2D (Y Dimension ignored)
    template <typename T, typename NODE, typename S>
    class CellVTI_PSV {
    public:
        CellVTI_PSV(const size_t n) :
        sign(1.0),
        Vp0(std::vector<T>(n)),
        Vs0(std::vector<T>(n)),
        epsilon(std::vector<T>(n)),
        delta(std::vector<T>(n)) {
        }

        void setVp0(const std::vector<T>& s) {
            if ( Vp0.size() != s.size() ) {
                throw std::length_error("Error: Vp0 vectors of incompatible size.");
            }
            Vp0 = s;
        }

        void setVs0(const std::vector<T>& s) {
            if ( Vs0.size() != s.size() ) {
                throw std::length_error("Error: Vs0 vectors of incompatible size.");
            }
            Vs0 = s;
        }

        void setEpsilon(const std::vector<T>& s) {
            if ( epsilon.size() != s.size() ) {
                throw std::length_error("Error: epsilon vectors of incompatible size.");
            }
            epsilon = s;
        }

        void setDelta(const std::vector<T>& s) {
            if ( delta.size() != s.size() ) {
                throw std::length_error("Error: delta vectors of incompatible size.");
            }
            delta = s;
        }

        void setPhase(const int p) {
            if ( p==1 ) sign = 1.;  // P wave
            else sign = -1.;        // SV wave
        }

        void setSlowness(const std::vector<T>& s) {
            throw std::logic_error("Error: slowness not defined for CellVTI_PSV.");
        }

        const T getSlowness(const size_t i) const {
            throw std::logic_error("Error: slowness not defined for CellVTI_PSV.");
        }

        void setXi(const std::vector<T>& s) {
            throw std::logic_error("Error: xi not defined for CellVTI_PSV.");
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for CellVTI_PSV.");
        }

        void setGamma(const std::vector<T>& s) {
            throw std::logic_error("Error: gamma not defined for CellVTI_PSV.");
        }

        void setS2(const std::vector<T>& r) {
            throw std::logic_error("Error: s2 not defined for CellVTI_PSV.");
        }
    
        void setS4(const std::vector<T>& r) {
            throw std::logic_error("Error: s4 not defined for CellVTI_PSV.");
        }

        T computeDt(const S& source, const S& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T theta = atan2(node.x - source.x, node.z - source.z);
            T f = 1. - (Vs0[cellNo]*Vs0[cellNo]) / (Vp0[cellNo]*Vp0[cellNo]);

            T tmp = 1. + (2.*epsilon[cellNo]*sin(theta)*sin(theta)) / f;

            tmp = 1. + epsilon[cellNo]*sin(theta)*sin(theta) - f/2. +
            sign*f/2.*sqrt( tmp*tmp - (2.*(epsilon[cellNo]-delta[cellNo])*sin(2.*theta)*sin(2.*theta))/f );

            T v = Vp0[cellNo] * sqrt( tmp );
            return source.getDistance( node ) / v;
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T theta = atan2(node.x - source.getX(), node.z - source.getZ());
            T f = 1. - (Vs0[cellNo]*Vs0[cellNo]) / (Vp0[cellNo]*Vp0[cellNo]);

            T tmp = 1. + (2.*epsilon[cellNo]*sin(theta)*sin(theta)) / f;

            tmp = 1. + epsilon[cellNo]*sin(theta)*sin(theta) - f/2. +
            sign*f/2.*sqrt( tmp*tmp - (2.*(epsilon[cellNo]-delta[cellNo])*sin(2.*theta)*sin(2.*theta))/f );

            T v = Vp0[cellNo] * sqrt( tmp );
            return source.getDistance( node ) / v;
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T theta = atan2(node.getX() - source.getX(), node.getZ() - source.getZ());
            T f = 1. - (Vs0[cellNo]*Vs0[cellNo]) / (Vp0[cellNo]*Vp0[cellNo]);

            T tmp = 1. + (2.*epsilon[cellNo]*sin(theta)*sin(theta)) / f;

            tmp = 1. + epsilon[cellNo]*sin(theta)*sin(theta) - f/2. +
            sign*f/2.*sqrt( tmp*tmp - (2.*(epsilon[cellNo]-delta[cellNo])*sin(2.*theta)*sin(2.*theta))/f );

            T v = Vp0[cellNo] * sqrt( tmp );
            return source.getDistance( node ) / v;
        }

        void computeDistance(const NODE& source, const S& node,
                             siv<T>& cell) const {
            assert(false);  // we should not end up here
            cell.v  = std::sqrt((node.x - source.getX())*(node.x - source.getX()) +
                                (node.z - source.getZ())*(node.z - source.getZ()));
        }
        void computeDistance(const NODE& source, const S& node,
                             siv2<T>& cell) const {
            cell.v  = std::abs(node.x - source.getX());
            cell.v2 = std::abs(node.z - source.getZ());
        }

    private:
        T sign;
        std::vector<T> Vp0;
        std::vector<T> Vs0;
        std::vector<T> epsilon;
        std::vector<T> delta;
    };



    //  VTI anisotropy, SH phase, in 2D (Y Dimension ignored)
    template <typename T, typename NODE, typename S>
    class CellVTI_SH {
    public:
        CellVTI_SH(const size_t n) :
        Vs0(std::vector<T>(n)),
        gamma(std::vector<T>(n)) {
        }

        void setVs0(const std::vector<T>& s) {
            if ( Vs0.size() != s.size() ) {
                throw std::length_error("Error: Vs0 vectors of incompatible size.");
            }
            Vs0 = s;
        }

        void setGamma(const std::vector<T>& s) {
            if ( gamma.size() != s.size() ) {
                throw std::length_error("Error: gamma vectors of incompatible size.");
            }
            gamma = s;
        }

        void setSlowness(const std::vector<T>& s) {
            throw std::logic_error("Error: slowness not defined for CellVTI_SH.");
        }

        const T getSlowness(const size_t i) const {
            throw std::logic_error("Error: slowness not defined for CellVTI_SH.");
        }

        void setXi(const std::vector<T>& s) {
            throw std::logic_error("Error: xi not defined for CellVTI_SH.");
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for CellVTI_SH.");
        }

        void setVp0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vp0 not defined for CellVTI_SH.");
        }

        void setDelta(const std::vector<T>& s) {
            throw std::logic_error("Error: delta not defined for CellVTI_SH.");
        }

        void setEpsilon(const std::vector<T>& s) {
            throw std::logic_error("Error: epsilon not defined for CellVTI_SH.");
        }

        void setS2(const std::vector<T>& r) {
            throw std::logic_error("Error: s2 not defined for CellVTI_SH.");
        }
    
        void setS4(const std::vector<T>& r) {
            throw std::logic_error("Error: s4 not defined for CellVTI_SH.");
        }

        T computeDt(const S& source, const S& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T theta = atan2(node.x - source.x, node.z - source.z);
            T v = Vs0[cellNo] * sqrt(1. + 2.*gamma[cellNo]*sin(theta)*sin(theta));
            return source.getDistance( node ) / v;
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T theta = atan2(node.x - source.getX(), node.z - source.getZ());
            T v = Vs0[cellNo] * sqrt(1. + 2.*gamma[cellNo]*sin(theta)*sin(theta));
            return source.getDistance( node ) / v;
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T theta = atan2(node.getX() - source.getX(), node.getZ() - source.getZ());
            T v = Vs0[cellNo] * sqrt(1. + 2.*gamma[cellNo]*sin(theta)*sin(theta));
            return source.getDistance( node ) / v;
        }

        void computeDistance(const NODE& source, const S& node,
                             siv<T>& cell) const {
            assert(false);  // we should not end up here
            cell.v  = std::sqrt((node.x - source.getX())*(node.x - source.getX()) +
                                (node.z - source.getZ())*(node.z - source.getZ()));
        }
        void computeDistance(const NODE& source, const S& node,
                             siv2<T>& cell) const {
            cell.v  = std::abs(node.x - source.getX());
            cell.v2 = std::abs(node.z - source.getZ());
        }

    private:
        std::vector<T> Vs0;
        std::vector<T> gamma;
    };


    template <typename T, typename NODE, typename S>
    class CellWeaklyAnelliptical {
    public:
        CellWeaklyAnelliptical(const size_t n) :
        v0(std::vector<T>(n)),
        s2(std::vector<T>(n)),
        s4(std::vector<T>(n)) {
        }
    
        const T getSlowness(const size_t i) const {
            return 1. / v0.at(i);
        }

        void setSlowness(const std::vector<T>& s) {
            if ( v0.size() != s.size() ) {
                throw std::length_error("Error: slowness vectors of incompatible size.");
            }
            for ( size_t n=0; n<v0.size(); ++n ) {
                v0[n] = 1. / s[n];
            }
        }
    
        void setS2(const std::vector<T>& r) {
            if ( s2.size() != r.size() ) {
                throw std::length_error("Error: s2 vectors of incompatible size.");
            }
            s2 = r;
        }
    
        void setS4(const std::vector<T>& r) {
            if ( s4.size() != r.size() ) {
                throw std::length_error("Error: s4 vectors of incompatible size.");
            }
            s4 = r;
        }

        void setXi(const std::vector<T>& s) {
            throw std::logic_error("Error: xi not defined for CellWeaklyAnelliptical.");
        }

        void setChi(const std::vector<T>& s) {
            throw std::logic_error("Error: chi not defined for CellWeaklyAnelliptical.");
        }

        void setPsi(const std::vector<T>& s) {
            throw std::logic_error("Error: psi not defined for CellWeaklyAnelliptical.");
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for CellWeaklyAnelliptical.");
        }

        void setVp0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vp0 not defined for CellWeaklyAnelliptical.");
        }

        void setVs0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vs0 not defined for CellWeaklyAnelliptical.");
        }

        void setDelta(const std::vector<T>& s) {
            throw std::logic_error("Error: delta not defined for CellWeaklyAnelliptical.");
        }

        void setEpsilon(const std::vector<T>& s) {
            throw std::logic_error("Error: epsilon not defined for CellWeaklyAnelliptical.");
        }

        void setGamma(const std::vector<T>& s) {
            throw std::logic_error("Error: gamma not defined for CellWeaklyAnelliptical.");
        }

        T computeDt(const S& source, const S& node,
                    const size_t cellNo) const {
            T v = get_energy_vel(node.x - source.x, node.z - source.z, cellNo);
            return source.getDistance( node ) / v;
        }
    
        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            T v = get_energy_vel(node.x - source.getX(), node.z - source.getZ(), cellNo);
            return source.getDistance( node ) / v;
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            T v = get_energy_vel(node.getX() - source.getX(), node.getZ() - source.getZ(), cellNo);
            return source.getDistance( node ) / v;
        }
    
        void computeDistance(const NODE& source, const S& node,
                             siv<T>& cell) const {
            assert(false);  // we should not end up here
            cell.v  = std::sqrt((node.x - source.getX())*(node.x - source.getX()) +
                                (node.z - source.getZ())*(node.z - source.getZ()));
        }
        void computeDistance(const NODE& source, const S& node,
                             siv2<T>& cell) const {
            cell.v  = std::abs(node.x - source.getX());
            cell.v2 = std::abs(node.z - source.getZ());
        }
        
    private:
        std::vector<T> v0;
        std::vector<T> s2;
        std::vector<T> s4;
        
        T get_energy_vel(const T dx, const T dz, const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T sin_theta = sin( atan2(dx, dz) );
            sin_theta *= sin_theta;  // square
            return v0[cellNo] * (1. + (s2[cellNo] + s4[cellNo] * sin_theta) * sin_theta);
        }
    };


    // Elliptical anisotropy in 3D

    template <typename T, typename NODE, typename S>
    class CellElliptical3D {
    public:
        CellElliptical3D(const size_t n) :
        slowness(std::vector<T>(n)),
        chi(std::vector<T>(n)),
        psi(std::vector<T>(n)) {
        }

        void setSlowness(const std::vector<T>& s) {
            if ( slowness.size() != s.size() ) {
                throw std::length_error("Error: slowness vectors of incompatible size.");
            }
            slowness = s;
        }

        const T getSlowness(const size_t i) const {
            return slowness.at(i);
        }

        void setChi(const std::vector<T>& s) {
            if ( chi.size() != s.size() ) {
                throw std::length_error("Error: chi vectors of incompatible size.");
            }
            for ( size_t n=0; n<chi.size(); ++n ) {
                chi[n] = s[n]*s[n];
            }
        }

        void setPsi(const std::vector<T>& s) {
            if ( psi.size() != s.size() ) {
                throw std::length_error("Error: psi vectors of incompatible size.");
            }
            for ( size_t n=0; n<psi.size(); ++n ) {
                psi[n] = s[n]*s[n];
            }
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for CellElliptical3D.");
        }

        void setVp0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vp0 not defined for CellElliptical3D.");
        }

        void setVs0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vs0 not defined for CellElliptical3D.");
        }

        void setDelta(const std::vector<T>& s) {
            throw std::logic_error("Error: delta not defined for CellElliptical3D.");
        }

        void setEpsilon(const std::vector<T>& s) {
            throw std::logic_error("Error: epsilon not defined for CellElliptical3D.");
        }

        void setGamma(const std::vector<T>& s) {
            throw std::logic_error("Error: gamma not defined for CellElliptical3D.");
        }

        T computeDt(const S& source, const S& node,
                    const size_t cellNo) const {
            T lx = node.x - source.x;
            T ly = node.y - source.y;
            T lz = node.z - source.z;
            return slowness[cellNo] * std::sqrt( chi[cellNo]*lx*lx + psi[cellNo]*ly*ly + lz*lz );
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            T lx = node.x - source.getX();
            T ly = node.y - source.getY();
            T lz = node.z - source.getZ();
            return slowness[cellNo] * std::sqrt( chi[cellNo]*lx*lx + psi[cellNo]*ly*ly + lz*lz );
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            T lx = node.getX() - source.getX();
            T ly = node.getY() - source.getY();
            T lz = node.getZ() - source.getZ();
            return slowness[cellNo] * std::sqrt( chi[cellNo]*lx*lx + psi[cellNo]*ly*ly + lz*lz );
        }

    private:
        std::vector<T> slowness;  // this vector contains sz
        std::vector<T> chi;       // anisotropy ratio, chi = sx / sz, *** squared ***
        std::vector<T> psi;       // anisotropy ratio, psi = sy / sz, *** squared ***
    };



    //  VTI anisotropy, P or SV phase, in 2D (Y Dimension ignored)
    template <typename T, typename NODE, typename S>
    class CellVTI_PSV3D {
    public:
        CellVTI_PSV3D(const size_t n) :
        sign(1.0),
        Vp0(std::vector<T>(n)),
        Vs0(std::vector<T>(n)),
        epsilon(std::vector<T>(n)),
        delta(std::vector<T>(n)) {
        }

        void setVp0(const std::vector<T>& s) {
            if ( Vp0.size() != s.size() ) {
                throw std::length_error("Error: Vp0 vectors of incompatible size.");
            }
            Vp0 = s;
        }

        void setVs0(const std::vector<T>& s) {
            if ( Vs0.size() != s.size() ) {
                throw std::length_error("Error: Vs0 vectors of incompatible size.");
            }
            Vs0 = s;
        }

        void setEpsilon(const std::vector<T>& s) {
            if ( epsilon.size() != s.size() ) {
                throw std::length_error("Error: epsilon vectors of incompatible size.");
            }
            epsilon = s;
        }

        void setDelta(const std::vector<T>& s) {
            if ( delta.size() != s.size() ) {
                throw std::length_error("Error: delta vectors of incompatible size.");
            }
            delta = s;
        }

        void setPhase(const int p) {
            if ( p==1 ) sign = 1.;  // P wave
            else sign = -1.;        // SV wave
        }

        void setXi(const std::vector<T>& s) {
            throw std::logic_error("Error: xi not defined for CellVTI_PSV3D.");
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for CellVTI_PSV3D.");
        }

        void setGamma(const std::vector<T>& s) {
            throw std::logic_error("Error: gamma not defined for CellVTI_PSV3D.");
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T lx = node.x - source.getX();
            T ly = node.y - source.getY();
            lx = std::sqrt( lx*lx + ly*ly ); // horizontal distance
            T theta = atan2(lx, node.z - source.getZ());
            T f = 1. - (Vs0[cellNo]*Vs0[cellNo]) / (Vp0[cellNo]*Vp0[cellNo]);

            T tmp = 1. + (2.*epsilon[cellNo]*sin(theta)*sin(theta)) / f;

            tmp = 1. + epsilon[cellNo]*sin(theta)*sin(theta) - f/2. +
            sign*f/2.*sqrt( tmp*tmp - (2.*(epsilon[cellNo]-delta[cellNo])*sin(2.*theta)*sin(2.*theta))/f );

            T v = Vp0[cellNo] * sqrt( tmp );
            return source.getDistance( node ) / v;
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T lx = node.getX() - source.getX();
            T ly = node.getY() - source.getY();
            lx = std::sqrt( lx*lx + ly*ly ); // horizontal distance
            T theta = atan2(lx, node.getZ() - source.getZ());
            T f = 1. - (Vs0[cellNo]*Vs0[cellNo]) / (Vp0[cellNo]*Vp0[cellNo]);

            T tmp = 1. + (2.*epsilon[cellNo]*sin(theta)*sin(theta)) / f;

            tmp = 1. + epsilon[cellNo]*sin(theta)*sin(theta) - f/2. +
            sign*f/2.*sqrt( tmp*tmp - (2.*(epsilon[cellNo]-delta[cellNo])*sin(2.*theta)*sin(2.*theta))/f );

            T v = Vp0[cellNo] * sqrt( tmp );
            return source.getDistance( node ) / v;
        }

    private:
        T sign;
        std::vector<T> Vp0;
        std::vector<T> Vs0;
        std::vector<T> epsilon;
        std::vector<T> delta;
    };



    //  VTI anisotropy, SH phase, in 2D (Y Dimension ignored)
    template <typename T, typename NODE, typename S>
    class CellVTI_SH3D {
    public:
        CellVTI_SH3D(const size_t n) :
        Vs0(std::vector<T>(n)),
        gamma(std::vector<T>(n)) {
        }

        void setVs0(const std::vector<T>& s) {
            if ( Vs0.size() != s.size() ) {
                throw std::length_error("Error: Vs0 vectors of incompatible size.");
            }
            Vs0 = s;
        }

        void setGamma(const std::vector<T>& s) {
            if ( gamma.size() != s.size() ) {
                throw std::length_error("Error: gamma vectors of incompatible size.");
            }
            gamma = s;
        }

        void setXi(const std::vector<T>& s) {
            throw std::logic_error("Error: xi not defined for CellVTI_SH3D.");
        }

        void setTiltAngle(const std::vector<T>& s) {
            throw std::logic_error("Error: TiltAngle not defined for CellVTI_SH3D.");
        }

        void setVp0(const std::vector<T>& s) {
            throw std::logic_error("Error: Vp0 not defined for CellVTI_SH3D.");
        }

        void setDelta(const std::vector<T>& s) {
            throw std::logic_error("Error: delta not defined for CellVTI_SH3D.");
        }

        void setEpsilon(const std::vector<T>& s) {
            throw std::logic_error("Error: epsilon not defined for CellVTI_SH3D.");
        }

        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T lx = node.x - source.getX();
            T ly = node.y - source.getY();
            lx = std::sqrt( lx*lx + ly*ly ); // horizontal distance
            T theta = atan2(lx, node.z - source.getZ());
            T v = Vs0[cellNo] * sqrt(1. + 2.*gamma[cellNo]*sin(theta)*sin(theta));
            return source.getDistance( node ) / v;
        }

        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T lx = node.getX() - source.getX();
            T ly = node.getY() - source.getY();
            lx = std::sqrt( lx*lx + ly*ly ); // horizontal distance
            T theta = atan2(lx, node.getZ() - source.getZ());
            T v = Vs0[cellNo] * sqrt(1. + 2.*gamma[cellNo]*sin(theta)*sin(theta));
            return source.getDistance( node ) / v;
        }

    private:
        std::vector<T> Vs0;
        std::vector<T> gamma;
    };

    template <typename T, typename NODE, typename S>
    class CellWeaklyAnelliptical3D {
    public:
        CellWeaklyAnelliptical3D(const size_t n) :
        v0(std::vector<T>(n)),
        s2(std::vector<T>(n)),
        s4(std::vector<T>(n)) {
        }

        void setV0(const std::vector<T>& v) {
            if ( v0.size != v.size() ) {
                throw std::length_error("Error: velocity vectors of incompatible size.");
            }
            v0 = v;
        }
        
        void setS2(const std::vector<T>& r) {
            if ( s2.size != r.size() ) {
                throw std::length_error("Error: s2 vectors of incompatible size.");
            }
            s2 = r;
        }
        
        void setS4(const std::vector<T>& r) {
            if ( s4.size != r.size() ) {
                throw std::length_error("Error: s4 vectors of incompatible size.");
            }
            s4 = r;
        }
        
        T computeDt(const NODE& source, const S& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T lx = node.x - source.getX();
            T ly = node.y - source.getY();
            lx = std::sqrt( lx*lx + ly*ly ); // horizontal distance
            T v = get_energy_vel(lx, node.z - source.getZ(), cellNo);
            return source.getDistance( node ) / v;
        }
        
        T computeDt(const NODE& source, const NODE& node,
                    const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T lx = node.getX() - source.getX();
            T ly = node.getY() - source.getY();
            lx = std::sqrt( lx*lx + ly*ly ); // horizontal distance
            T v = get_energy_vel(lx, node.getZ() - source.getZ(), cellNo);
            return source.getDistance( node ) / v;
        }
        
    private:
        std::vector<T> v0;
        std::vector<T> s2;
        std::vector<T> s4;
        
        T get_energy_vel(const T dx, const T dz, const size_t cellNo) const {
            // theta: angle w/r to vertical axis
            T sin_theta = sin( atan2(dx, dz) );
            sin_theta *= sin_theta;  // square
            return v0[cellNo] * (1. + (s2[cellNo] + s4[cellNo] * sin_theta) * sin_theta);
        }

    };

}

#endif /* Cell_h */
